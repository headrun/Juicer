from juicer.utils import *
from dateutil import parser

class Huxiu(JuicerSpider):
    name = "huxiu_china"
    start_urls = ['http://www.huxiu.com/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="article-box-ctt"]//h4//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//td//div//p//text()'))
        dt_added = textify(hdoc.select('//time[@id="pubtime_baidu"]//text()'))
        author = textify(hdoc.select('//span[@class="recommenders"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

