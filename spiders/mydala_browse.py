from juicer.utils import *

class MydalaBrowseSpider(JuicerSpider):
    name = 'mydala_browse'
    allowed_domains = ['mydala.com']
    start_urls = 'http://www.mydala.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="cities"]//a[not(contains(@href, "/deals-allindia"))]/@href',\
                                 '/ul[@id="nav-dropdown"]//li//a[contains(@class, "navOuter")][not(contains(@href, "bid-deals"))]/@href',\
                                 '//div[@class="pagination fltRight suffix-8"]//a[contains(text(), "next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="deal-showcase"]//a[@class="deal-showcase-image-wrapper"]/@href'], response)

        for url in terminal_urls: get_page('mydala_terminal', url)
