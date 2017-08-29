from juicer.utils import *
from dateutil import parser
class ToyotaIndiaNews(JuicerSpider):
    name = 'toyota_india_news'
    start_urls = ['http://www.toyotabharat.com/inen/news/2014/index.aspx']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td//p[@align="center"]//strong//text()'))
        #text
        text = textify(hdoc.select('//tr/td[@class="articlesubheading"]//p/text()'))
        if not text:
            text = textify(hdoc.select('//td[@class="articlesubheading"]'))
        #date
        dt_added = textify(hdoc.select('//td[@class="articlesubheading"]/p/strong/text()')[0])
        if u'\u2019' in dt_added:
            dt_added = dt_added.replace(u'\u2019', ' ')
        #dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        print "TITLE::::",xcode(title)
        print "TEXT:::::",xcode(text)
        print "DATE:::",xcode(dt_added)
        print "URL::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        #yield item.process()


