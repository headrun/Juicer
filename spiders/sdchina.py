from juicer.utils import *
from dateutil import parser

class SdChina(JuicerSpider):
    name = "sdchina"
    start_urls = ['http://3g.sdchina.com/news/','http://3g.sdchina.com/minsheng/','http://3g.sdchina.com/auto/','http://3g.sdchina.com/sports/','http://3g.sdchina.com/leisure/','http://3g.sdchina.com/edu/','http://3g.sdchina.com/house/','http://3g.sdchina.com/ent/','http://3g.sdchina.com/tour/','http://3g.sdchina.com/health/','http://3g.sdchina.com/news/#']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//article[@class="topNews"]//ul[@class="clearfix"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="maina"]//h2//text()'))
        text = textify(hdoc.select('//div[@class="mainb"]/p/text()'))
        dt_added = textify(hdoc.select('//div[@class="maina"]//h3//text()'))
        dt_added = dt_added.split(u'\uff1a')
        dt_added = dt_added[2]
        author = textify(hdoc.select('//h5//text()'))
        author = author.split(u'\uff1a')
        author.pop(0)
        if not author:
            author = ""
        else:
            author = author[0]
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

