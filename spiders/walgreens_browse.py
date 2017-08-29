from juicer.utils import *

class WalgreensSpider(JuicerSpider):
    name = 'walgreens_browse'
    allowed_domains = ['walgreens.com']
    start_urls = 'http://www.walgreens.com/store/catalog/shopLanding?tab=view_all'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@class="link-arrow-list top-level"]//li//a/@href',\
                                 '//div[@id="paginationBtm"]//a[@title="Next Page"]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="product-name"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('ID=')[1].split('prod')[1][:-1]
            get_page('walgreens_terminal', url, sk=sk)
