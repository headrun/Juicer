from juicer.utils import *
from dateutil import parser

class Qingdaonews(JuicerSpider):
    name = "qingdaonews_china"
    start_urls = ['http://news.qingdaonews.com/shehui/','http://news.qingdaonews.com/guoji/','http://news.qingdaonews.com/zhongguo/','http://sports.qingdaonews.com/node/node_92799.htm','http://news.qingdaonews.com/qingdao/node_26974.htm','http://auto.qingdaonews.com/node/node_18037.htm','http://auto.qingdaonews.com/node/node_91814.htm','http://auto.qingdaonews.com/node/node_91813.htm','http://auto.qingdaonews.com/node/node_91132.htm','http://auto.qingdaonews.com/node/node_91131.htm','http://dazhe.qingdaonews.com/node/node_133377.htm','http://dazhe.qingdaonews.com/node/node_133377.htm','http://edu.qingdaonews.com/node/node_16872.htm','http://edu.qingdaonews.com/node/node_41090.htm','http://edu.qingdaonews.com/node/node_41101.htm','http://health.qingdaonews.com/node/node_37739.htm','http://www.qingdaonews.com/node/node_90787.htm','http://www.qingdaonews.com/node/node_90786.htm','http://www.qingdaonews.com/node/node_90785.htm','http://www.qingdaonews.com/node/node_90784.htm','http://news.qingdaonews.com/qingdao/node_93394.htm','http://news.qingdaonews.com/qingdao/','http://www.qingdaonews.com/node/node_90786.htm','http://www.qingdaonews.com/node/node_90785.htm','http://www.qingdaonews.com/node/node_90784.htm','http://www.qingdaonews.com/node/node_90783.htm','http://www.qingdaonews.com/node/node_90787.htm','http://baby.qingdaonews.com/node/node_18713.htm','http://baby.qingdaonews.com/node/node_18689.htm']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="main"]//ul[@class="newslist14px"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@id="endText"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//td//p//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//div[@class="sourcetime"]/text()'))
        author = textify(hdoc.select('//span[@id="author_baidu"]//text()'))
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ''.join(author)
        if not author:
            author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
            author = author.split(u'\uff1a')
            author.pop(0)
            author = ''.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

