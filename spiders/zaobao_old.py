from juicer.utils import *
from dateutil import parser

class Zaobao_Site(JuicerSpider):
    name = "zaobao_site"
    start_urls = ['http://www.zaobao.com.sg/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav navbar-nav jewel"]//li/a[not(contains(@href,"#search"))]/@href').extract()
        for category in categories:
             if 'http' not in category:
                category = 'http://www.zaobao.com.sg/' + category
                import pdb;pdb.set_trace()
                #yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes =  hdoc.select('//div[@class=" row list"]') or hdoc.select('//ul[@class="bananas"]/li')
        for node in nodes:
            date = textify(node.select('.//span[@class="datestamp"]//text()')) or textify(node.select('.//a/em/text()').extract())[:2]+':'+textify(node.select('.//a/em/text()').extract())[2:]
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('.//a/@href'))
            if 'http' not in link: link = 'http://www.zaobao.com.sg' + link
            yield Request(link,self.parse_details,response)

        node2 = hdoc.select('//div[@class="post-detail"]')
        for node in node2:
            link = textify(node.select('./a/@href'))
            date = textify(node.select('./span[@class="datestamp"]/text()'))
            time = textify(node.select('./span[@class="datestamp"]/em/text()'))
            final_date = date + ' ' + time
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            if 'http' not in link: link = 'http://www.zaobao.com.sg' + link
            yield Request(link,self.parse_details,response)

        next_pg = textify(hdoc.select('//div[@class="item-list"]//li[contains(@class, "pager-next")]/a/@href'))
        if 'http' not in next_pg: next_pg = 'http://www.zaobao.com.sg' + next_pg
        yield Request(next_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc= HTML(response)
        title = textify(hdoc.select('//div[@class="body-content"]/h1/text()'))
        text = textify(hdoc.select('//div[@id="FineDining"]/p//text()'))
        author = textify(hdoc.select('//span[contains(@class,"contributor meta")]/a/text()'))
        author_url= textify(hdoc.select('//span[contains(@class,"contributor meta")]/a/@href'))
        if 'http' not in author_url:
            author_url = 'http://www.zaobao.com.sg' + author_url
        date = textify(hdoc.select('//span[@class="datestamp"]//text()'))
        date = '-'.join(re.findall('(\d+)',date)[:3])
        time = textify(hdoc.select('//span[@class="datestamp"]/em/text()').extract())
        final_date = date + ' '+ time
        dt_added = get_timestamp(parse_date(xcode(final_date)) - datetime.timedelta(hours=8))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'author',xcode(author)
        print 'author_url',xcode(author_url)
        print 'dt_added',xcode(dt_added)

'''     item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('author',{'name':xcode(author), 'url':author_url})
        item.set('dt_added', dt_added) '''

