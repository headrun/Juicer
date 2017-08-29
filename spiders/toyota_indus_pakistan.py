from juicer.utils import *
from dateutil import parser
class ToyotaIndusPakistan(JuicerSpider):
    name = 'toyota_indus_pakistan'
    start_urls = ['http://www.toyota-indus.com/news-events/']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//h3//a[@class="fancybox"]//@href')
        for url in urls:
            title = textify(url.select('.//h3//text()'))
            print "title",title
        #for url in urls:
        #    yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('.//h3/text()'))
        text = textify(hdoc.select('.//p/text()'))
        #dt_added = textify(hdoc.select(''))
        #author = textify(hdoc.select())
        #dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        print "TITLE::::",xcode(title)
        print "TEXT:::::",xcode(text)
       # print "DATE:::",xcode(dt_added)
        print "URL::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        #yield item.process()


