from juicer.utils import *
from dateutil import parser

class FordPhilippines(JuicerSpider):
    name = 'ford_philippines'
    start_urls = ['http://www.ford.com.ph/buying/events-calendar']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="content"]//h3//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="cms"]//h3//text()'))
        text = textify(hdoc.select('//div[@class="cms"]//p//text()')[1:])
        dt_added = textify(hdoc.select('//p[@class="date"]//text()'))
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()
