from juicer.utils import *

class TruliaSpider(JuicerSpider):
    name = 'trulia_browse'
    allowed_domains = ['trulia.com']
    start_urls = 'http://www.trulia.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="newsfeed_item clearfix"]//div[@class="fleft"]//a/@href',\
                                 '//span[@class="pg_link_cur"]//following-sibling::a[@class="pg_link"][1]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="row_address_details clearfix"]//div[@class="address_section"]//a/@href', response)
        for url in terminal_urls:
            get_page('trulia_terminal', url)
