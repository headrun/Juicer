from juicer.utils import *
from dateutil import parser

class Sznews(JuicerSpider):
    name = "sznews_china"
    start_urls = ['http://news.sznews.com/node_150186.htm','http://news.sznews.com/node_31202.htm','http://news.sznews.com/node_150127.htm','http://news.sznews.com/node_31220.htm','http://news.sznews.com/node_150166.htm','http://news.sznews.com/node_150128.htm','http://news.sznews.com/node_31200.htm','http://news.sznews.com/node_134906.htm','http://news.sznews.com/node_134907.htm','http://news.sznews.com/node_150126.htm']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="listw mt10"]//ul[@class="txtul"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        text = textify(hdoc.select('//div[@class="new_txt"]//p//text()'))
        author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
        if author:
            author = author.split(u'\uff1a')[1]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode(author))
        item.set('url', response.url)
        yield item.process()

