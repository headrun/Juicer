from juicer.utils import *

class HolidaylettingsSpider(JuicerSpider):
    name = 'holidaylettings_browse'
    allowed_domains = ['holidaylettings.com']
    start_urls = 'http://www.holidaylettings.co.uk/search.asp?'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a[@class="dpreg"]/@href',\
                                 '//td[@id="search_page"]//td[@class="button"]/a[contains(img/@src,"arrow_right.png")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//a[@class="srp_property_link"]/@href'], response)

        for url in terminal_urls:
            sk = url.split('/')[-1]
            get_page('holidaylettings_terminal', url, sk=sk)
