from juicer.utils import *
from dateutil import parser
class HondaThailana(JuicerSpider):
    name = 'honda_thailand'
    start_urls = ['http://www.honda.co.th/en/newsrelease']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="list-news"]//h2//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//article[@class="detail"]//h4//text()'))
        text = textify(hdoc.select('//article[@class="detail"]//p//text()')[1:])
        dt_added = textify(hdoc.select('//p[@class="date"]//text()'))
        print " "
        #author = textify(hdoc.select())
        #dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        print "TITLE::::",xcode(title)
        print "TEXT:::::",xcode(text)
        print "DATE:::",xcode(dt_added)
        print "URL::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        #item.set('dt_added', dt_added)
        #yield item.process()


