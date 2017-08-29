from juicer.utils import *

class ReiSpider(JuicerSpider):
    name = 'rei_browse'
    allowed_domains = ['rei.com']
    start_urls = 'http://www.rei.com/categories'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@class="listStyle0 categoryToc"]//li//a/@href',\
                                 '//div[@class="gearHdr"]//a/@href',\
                                 '//li[@class="sbTitle"]//a/@href',\
                                 '//li[@class="pagination"]//img[@title="next"]//parent::a/@href'], response)

        for url in urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls(['//div[@id="results"]//ul[@class="productBox"]//li[1]//a/@href'], response)
        for url in terminal_urls:
            sk = url.split('/product/')[-1].split('/')[0]
            get_page('rei_terminal', url, sk=sk)
