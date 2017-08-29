from juicer.utils import *

class Businessweekindonesia(JuicerSpider):
    name = "businessweekindonesia"
    start_urls = ['http://www.akosha.com/']

    def parse(self, response):
        hdoc = HTML(response)

        url = 'http://www.businessweekindonesia.com/article/post'
        payload = "tipe_search=-1&changing=1&date_index=&start=45&cat=-1"

        yield Request(url, self.parse_terminal, response, method="POST", body=payload)

    def parse_terminal(self, response):
        hdoc = HTML(response)


