from juicer.utils import *
from dateutil import parser

class  ClassName(JuicerSpider):
    name = 'spider_name'
    start_urls = ['']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('listing teminal urls')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select(''))
        text = textify(hdoc.select(''))
        dt_added = textify(hdoc.select(''))
        author = textify(hdoc.select(''))
        #dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        '''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()
        '''

