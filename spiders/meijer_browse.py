from juicer.utils import *

class MeijerSpider(JuicerSpider):
    name = 'meijer_browse'
    allowed_domains = ['meijer.com']
    start_urls = 'http://www.meijer.com/Site_Map.cms'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="Sitemap"]//dt//a/@href',\
                                 '//div[@class="options"]//ul//li//a/@href',\
                                 '//div[@class="options"]//ul//li[@class="selected"]//a/@href'], response)
        for url in urls: get_page(self.name, url)

        next_url = hdoc.select_urls(['//div[@class="paging cb"]//a[contains(text(), "Next Page ")]/@href'], response)
        if next_url:
            next_url = next_url[0]
            print next_url
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//p[@class="reduced nameWrapper"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('R-')[1]
            get_page('meijer_terminal', url, sk=sk)
