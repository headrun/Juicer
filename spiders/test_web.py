import httplib

from juicer.utils import *

class TestwebSpider(JuicerSpider):
    name = 'test_web'
    start_urls = 'http://testweb.juicer.headrun.com/data'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//li//@href', response)
        for url in urls:
            yield Request(url,self.parse,response)
