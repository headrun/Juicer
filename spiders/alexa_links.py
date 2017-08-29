from juicer.utils import *
from dateutil import parser

class AlexaLinks(JuicerSpider):
    name = 'alexa_links'
    start_urls = 'http://www.alexa.com/topsites/countries/ID'

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        output_file = 'Indonesiatopsites'
        links = hdoc.select('//div[@class="desc-container"]/p/a/@href').extract()
        for link in links:
            link = 'http://www.alexa.com' + link
            out_file = file(output_file,'ab+')
            out_file.write('%s\n'%link)
            out_file.close()

        nxt_page = textify(hdoc.select('//div[@class="alexa-pagination"]/a[@title="Next"]/@href'))
        if nxt_page:
            nxt_page = 'http://www.alexa.com' + nxt_page
            yield Request(nxt_page,self.parse,response)

