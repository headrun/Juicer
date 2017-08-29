from juicer.utils import *
from dateutil import parser
class MmpcPhilippines(JuicerSpider):
    name = 'mmpc_philippines'
    start_urls = ['http://www.mmpc.ph/news/2014/']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//ul[@class="paging"]//li//div[@class="ntitle"]//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td//p[@align="center"]/strong/text()'))
        if not title:
            title = textify(hdoc.select('//div[@class="style3"]//text()'))
        text = textify(hdoc.select('//td//p//text()'))
        print " "
        #author = textify(hdoc.select())
        #dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        print "TITLE::::",xcode(title)
        print "TEXT:::::",xcode(text)
        #print "DATE:::",xcode(dt_added)
        print "URL::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        #item.set('dt_added', dt_added)
        #yield item.process()


