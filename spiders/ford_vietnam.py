from juicer.utils import *
from dateutil import parser
class FordVietnam(JuicerSpider):
    name = 'ford_vietnam'
    start_urls = ['http://www.ford.com.vn/clb/news']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="content"]//div[@class="article ei-enabled"]//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="cms"]//h3//text()'))
        text = textify(hdoc.select('//div[@class="cms"]/p/text()')[1:])
        dt_added = textify(hdoc.select('//p[@class="date"]//text()'))
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


