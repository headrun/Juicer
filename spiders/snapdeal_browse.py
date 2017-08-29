from juicer.utils import *

class SnapdealBrowseSpider(JuicerSpider):
    name = 'snapdeal_browse'
    allowed_domains = ['snapdeal.com']
    start_urls = 'http://www.snapdeal.com/info/sitemap'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="column"]//ul//a/@href[contains(., "/deals")]',\
                                 '//div[contains(text(), "View all")]//parent::a/@href'], response)

        for url in urls: get_page(self.name,url)

        terminal_urls = hdoc.select_urls(['//div[@class="product_listing_heading"]//a/@href'], response)

        for url in terminal_urls: get_page('snapdeal_terminal', url)
