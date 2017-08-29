
from juicer.utils import *

class BollySpiceNewsBrowseSpider(JuicerSpider):
    name = 'bollyspicenews_browse'
    allow_domain = 'bollyspice.com'
    start_urls = 'http://bollyspice.com/category/news'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        next_urls = hdoc.select_urls('//div[@class="wp-pagenavi"]//a[@class="nextpostslink"]/@href', response)
        for url in next_urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls('//div[@class="contentsingle"]//h1/a/@href', response)
        for url in terminal_urls:
            get_page('bollyspicenews_terminal', url)

