from juicer.utils import *

class CabelasSpider(JuicerSpider):
    name = 'cabelas_browse'
    allowed_domains = ['cabelas.com']
    start_urls = 'http://www.cabelas.com/custserv/sitemap.jsp?WTz_l=Footer'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@class="megaMenuList"]//li//a/@href',\
                                 '//li[@class="active"]//ul//li//a/@href',\
                                 '//li[@class="active"]//ul//li//ul//li//a/@href',\
                                 '//a[contains(text(),"Next")]/@href[1]'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="itemInformation"]//strong//a/@href', response)
        for url in terminal_urls:
            get_page('cabelas_terminal', url)
