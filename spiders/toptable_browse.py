from juicer.utils import *

class ToptableSpider(JuicerSpider):
    name = 'toptable_browse'
    allowed_domains = ['toptable.com']
    start_urls = 'http://www.toptable.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="countries-container"]//ul//li//a/@href',\
                                 '//div[@class="menu-group location"]//ul//li//a[contains(text(),"All restaurants")]/@href',\
                                 '//div[@id="ctl00_Body_venueList_nextPageButton"]//a[contains(text(),"next")]/@href'], response)
        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="col-main-details"]//h3//a/@href', response)
        for url in terminal_urls:
            sk = url.split('id=')[1]
            get_page('toptable_terminal', url, sk=sk)
