from juicer.utils import *
from dateutil import parser
class HondaIndonesia(JuicerSpider):
    name = 'honda_indonesia'
    start_urls = ['http://www.honda-indonesia.com/newslist/']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td/p[@align="justify"]/a/@href')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//span[@class="regulartextdark"]/text()')[1])
        text = textify(hdoc.select('//td//p[@class="text-sub"]/text()'))
        dt_added = textify(hdoc.select('//span[@class="regulartextdark"]/text()')[0])
        #author = textify(hdoc.select())
        #dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        print "TITLE::::",xcode(title)
        print "TEXT:::::",xcode(text)
        print "DATE:::",xcode(dt_added)
        print "URL::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        #yield item.process()


