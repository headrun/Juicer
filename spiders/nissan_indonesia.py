from juicer.utils import *
from dateutil import parser
class NissanIndonesia(JuicerSpider):
    name = 'nissan_indonesia'
    start_urls = ['http://www.nissan.co.id/id-ID/News.aspx']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="articleList"]//div[@class="grid_3"]//a//@href')
        for url in urls:
            print url
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//section[@class="container"]//h1//text()'))
        text = textify(hdoc.select('//article[@class="richContentBlock"]//text()')[1:])
        dt_added = textify(hdoc.select('//div[@class="meta"]//span[@class="date"]//text()'))
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


