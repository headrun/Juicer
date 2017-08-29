from juicer.utils import *
from dateutil import parser

class Dbw(JuicerSpider):
    name = 'dbw_china'
    start_urls = ['']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select(''))
        text = textify(hdoc.select(''))
        dt_added = textify(hdoc.select(''))
        author = textify(hdoc.select(''))
        print "title::",xcode(title)
        print "text::",xcode(text)
        print "date:::",xcode(dt_added)
        print "author:",xcode(author)

        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        #yield item.process()
