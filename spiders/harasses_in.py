from juicer.utils import *
from dateutil import parser

class HarassedIn(JuicerSpider):
    name = 'harasses_in'
    start_urls = ['http://www.harassed.in/questions/']

    def parse(self,response):
        hdoc  = HTML(response)
        nodes = hdoc.select('//div[@class="ap-display-question-meta"]')
        for node in nodes:
            date = textify(node.select('.//time/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            link = textify(node.select('.//a/@href')[1])
            yield Request(link,self.parse_details,response)

            print '\n'
            print link
            print date
            print dt_added

        nxt_page = textify(hdoc.select('//a[@class="next page-numbers"]/@href'))
        if nxt_page:
            yield Request(nxt_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = hdoc.select('//h1[@class="title"]/text()')

