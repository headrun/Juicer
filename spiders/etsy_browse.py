from juicer.utils import *

class EtsySpider(JuicerSpider):
    name = 'etsy_browse'
    allowed_domains = ['etsy.com']
    start_urls = 'http://www.etsy.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@id="category-list"]//li//a/@href',\
                                 '//ul[@id="category-nav"]//li//a/@href',\
                                 '//p[@class="controls"]//a[@class="next"]/@href'], response)
        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//p[@class="listing-title"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('/listing/')[-1].split('/')[0]
            get_page('etsy_terminal', url, sk=sk)
