from juicer.utils import *
from dateutil import parser

class HondaphilPhilippines(JuicerSpider):
    name = 'hondaphil_philippines'
    start_urls = ['http://www.hondaphil.com/news/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="news newslist"]//ul//li/a/@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="inside-content news-inside-content"]//p//text()'))
        dt_added = textify(hdoc.select('//div[@class="date"]//text()'))

        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()


