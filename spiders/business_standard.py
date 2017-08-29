from juicer.utils import*
from dateutil import parser

class BusinessStandard(JuicerSpider):
    name = 'business_standard'
    start_urls = ['http://www.business-standard.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="select"]//a[contains(@id, "nav_menu")]/@href').extract()
        for category in categories:
            if 'http' not in category:
                category = 'http://www.business-standard.com' + category
                yield Request(category, self.parse_next, response)

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        urls = hdoc.select(hdoc.select('//ul[@class="aticle-txt "]') or hdoc.select('//div[@class="aticle-list"]/ul') or hdoc.select('//ul[@class="aticle-txt1"]') or ('//div[@class="listing-txt"]'))
        for url in urls:
            date = textify(url.select('./p[1]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5, minutes=30))
            if dt_added < get_current_timestamp()-86400*30:
                continue
            news_link = textify(url.select('./h2/a/@href'))
            if 'http' not in news_link:
                news_link = 'http://www.business-standard.com' + news_link
                yield Request(news_link,self.parse_details,response)

        next_page = textify(hdoc.select('//div[@class="next-colum"]/a/@href'))
        if 'http' not in next_page:
            next_page = 'http://www.business-standard.com' + next_page
            yield Request(next_page,self.parse_next,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="headline"]//text()'))
        text = textify(hdoc.select('//h2[@class="alternativeHeadline"]/text() | //span[@class="p-content"]//text()'))
        script_text= textify(hdoc.select('//span[@class="p-content"]//script[@type="text/javascript"]/text()'))
        text = text.replace(script_text,'')
        text = text.split('ALSO READ:')[0]
        author = ' & '.join(hdoc.select('//div[@class="last-update mT10"]//p/span/a//text()').extract())
        author_url = textify(hdoc.select('//div[@class="last-update mT10"]//p//a/@href'))
        if author_url!='':
            if 'http' not in author_url:
                author_url = 'http://www.business-standard.com' + author_url
            else:
                author_url = author_url
        date = textify(hdoc.select('//div[@class="last-update mT10"]//meta[@itemprop="datePublished"]/@content'))
        if not author:
            author = textify(hdoc.select('//p[@class="fL"]/span[1]'))
            if '|' in author: author = textify(author.split('|')[0].strip(" "))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5, minutes=30))
        if title == '' or text == '' or date == '': import pdb;pdb.set_trace()

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)
        print 'author',xcode(author)
        print 'author_url',xcode(author_url)

        '''
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'url':author_url,'name':xcode(author)})'''
