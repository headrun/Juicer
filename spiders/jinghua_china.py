from juicer.utils import *
from dateutil import parser

class Jinghua(JuicerSpider):
    name = "jinghua_china"
    start_urls = ['http://news.jinghua.cn/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="list"]//dl//dt//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="content_header"]//h1//text()'))
        text = textify(hdoc.select('//div[@id="container"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        author = textify(hdoc.select('//span[@id="jhEditor"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

