from juicer.utils import *

class MyntraSpider(JuicerSpider):
    name = 'myntra_browse'
    allowed_domains = ['myntra.com']
    start_urls = ['http://www.myntra.com/kids', 'http://www.myntra.com/women', 'http://www.myntra.com/men']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="pagination-links right"]//a/@href'], response)
        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="pagination-links right"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-2]
            get_page('myntra_terminal', url, sk=sk, data=123456)
