from juicer.utils import *
from dateutil import parser
import re

class Borotimes(JuicerSpider):
    name = "borotimes"
    start_urls = ['http://borotimes.com/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//article[@class="post"]//h2//a//@href')
        for url in urls:
            #print url
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="entry-title"]//span//text()'))
        text = textify(hdoc.select('//div[@class="entry-content"]//p//text()'))
        dt_added = textify(hdoc.select('//div[@class="entry-meta row-fluid"]//li//text()')[2])
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))
        import pdb;pdb.set_trace()


        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)

'''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(dt_added))
        item.set('url', response.url)
        yield item.process() '''

