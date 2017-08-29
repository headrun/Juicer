from juicer.utils import *

class AlibabaSpider(JuicerSpider):
    name = 'alibaba_browse'
    allowed_domains = ['alibaba.com']
    start_urls = 'http://www.alibaba.com/sitemap/product_categories.html'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//div[@class="column"]//ul[@class="narrow"]//li//a/@href',\
                                            '//a[@class="next-page page-btn"]/@href'], response)
        for navigation_url in navigation_urls:
            get_page(self.name, navigation_url)

        terminal_urls = hdoc.select_urls(['//div[@class="attr"]//h2//a/@href'], response)

        for terminal_url in terminal_urls:
            get_page('alibaba_terminal', terminal_url)
