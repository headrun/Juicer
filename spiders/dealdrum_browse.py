from juicer.utils import *

class DealdrumBrowseSpider(JuicerSpider):
    name = 'dealdrum_browse'
    allowed_domains = ['dealdrums.com']
    start_urls = 'http://hyderabad.dealdrums.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="a14gr1"]//a/@href',\
                                 '//div[@class="links"][contains(@style, "width: 360px;")]//a/@href',\
                                 '//div[@class="a16"]//a/@href',\
                                 '//div[@class="a12"]//a[contains(text(), "Next")]/@href'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="main-container"]//div[@class="a14"]//a/@href'], response)

        for url in terminal_urls:
            get_page('dealdrum_terminal', url)
