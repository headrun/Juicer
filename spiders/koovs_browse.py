from juicer.utils import *

class KoovsBrowseSpider(JuicerSpider):
    name = 'koovs_browse'
    allowed_domains = ['koovs.com']
    start_urls = 'http://www.koovs.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//li[@class="activeDrop"]/a/@href',\
                                 '//a[contains(text(), "Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="ProductBlk leftAlign"]/a/@href'], response)

        for url in terminal_urls: get_page('koovs_terminal', url)
