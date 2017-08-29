from juicer.utils import *

class CrazealBrowseSpider(JuicerSpider):
    name = 'crazeal_browse'
    allowed_domains = ['crazeal.com']
    start_urls = 'http://www.crazeal.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="boxPart boxMid"]//ul//li[not(contains(@class, " jGroupSelector"))]//a/@href',\
                                 '/ul[@id="nav-dropdown"]//li//a[contains(@class, "navOuter")][not(contains(@href, "bid-deals"))]/@href',\
                                 '//div[@class="pagination fltRight suffix-8"]//a[contains(text(), "next")]/@href'], response)

        for url in urls: get_page(self.name, url) 
        terminal_urls = hdoc.select_urls(['//div[@class="extraDealMulti"]//a/@href'], response)
        for url in terminal_urls: get_page('mydala_terminal', url)
