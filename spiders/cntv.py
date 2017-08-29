from juicer.utils import *
from dateutil import parser

class Cntv(JuicerSpider):
    name = "cntv_china"
    start_urls = ['']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('class="ecoA9805_con02"')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select(''))
        text = textify(hdoc.select(''))
        dt_added = textify(hdoc.select(''))
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        print "TITLE::::::::::::::::",xcode(title)
        print "TEXT:::::::::::::::::",xcode(text)
        print "DATE::::::::",xcode(dt_added)
        print "url:::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
       # item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()

