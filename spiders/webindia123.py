from juicer.utils import *
from dateutil import parser

class WebIndia123(JuicerSpider):
    name = 'webindia123'
    start_urls = ['http://news.webindia123.com/news/index.html']

    def parse(self,response):
        hdoc = HTML(response)
        category = hdoc.select('//div[@class="menu-list"]/a[contains(@href,"/news/")][not(contains(@href,"Releases.asp"))]/@href').extract()
        for link in category:
            if 'http' not in link:
                link = 'http://news.webindia123.com' + link
                yield Request(link,self.parse_next,response)

    def parse_next(self, response):
        hdoc = HTML(response)
        is_next = True
        urls = hdoc.select('//a[@id="head"]')
        for url in urls:
            final_url = textify(url.select('./@href').extract())
            date = textify(url.select('./parent::td/parent::tr/following-sibling::tr//div[@class]')).split('|')[-1].strip()
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*3:
                is_next = False
                continue

            if 'http:' not in final_url:
                final_url = '/'.join(response.url.split('/')[:-1])+'/'+ final_url
            yield Request(final_url, self.parse_details, response)

        next_pages = hdoc.select('//div[@class="s-left"]/a/@href').extract()
        if next_pages:
            import pdb;pdb.set_trace()
            response_url = response.url.split('/')[-1]
            url = re.findall('\w+.',response_url)[0].title()+ re.findall('\w+.',response_url)[-1]
            next_pgno = int(textify(re.findall('\d+',response_url)))
            next_pagenum = next_pgno + 1
            link = url.replace(str(next_pgno),str(next_pagenum))
            if link in next_pages:
                if 'http' not in link: next_pages = '/'.join(response.url.split('/')[:-1])+'/'+ link
            yield Request(next_pages,self.parse_next,response)

    def parse_details(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="head_line"]//text()'))
        text = textify(hdoc.select('//table[@width="100%"]/tr/td/text()') + hdoc.select('//table[@width="100%"]/tr/td/p/text()'))
        date = textify(hdoc.select('//td[@height="25"]//div[@class="d1"]//text()')).split ('|')[-1]
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))

        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()
