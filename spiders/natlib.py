from juicer.utils import *
from dateutil import parser

class Natlib(JuicerSpider):
    name = 'natlib'
    start_urls = 'http://natlib.govt.nz/'

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        links = hdoc.select('//div[@class="row"]//h3/a/@href')

        for link in links:
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="row panels"]//h3//text()'))
        text = textify(hdoc.select('//div[@class="row panels"]//p'))


