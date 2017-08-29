from juicer.utils import *
from dateutil import parser

class  ClassName(JuicerSpider):
    name = "tom_news"
    start_urls = ['http://news.tom.com/china/gat/index.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="main"]/div[@class="maincolb"]/ul//li/a/@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="PrintTxt"]/h1/text()'))
        text = textify(hdoc.select('//div[@id="content_body"]/div[@class="post"]//p/text()'))
        dt_added = textify(hdoc.select('//div[@id="content_body"]/p/text()'))
        author = textify(hdoc.select('//div[@class="operate"]/div[2]/text()'))
        #dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        print "title  :",xcode(title)
        print "date   :",xcode(dt_added)
        print "url    :",response.url
        print "author :",xcode(author)
        print "text   :",xcode(text)

        '''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()
        '''

