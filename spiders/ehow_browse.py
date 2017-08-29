from juicer.utils import *

class EhowSpider(JuicerSpider):
    name = 'ehow_browse'
    allowed_domains = ['http://www.ehow.com']
    start_urls = 'http://www.ehow.com'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//section[@id="BrowseHowTos"]//li/a/@href',\
                                 '//section[@class="FLC"]//li/a/@href',\
                                 '//section[@class="SidebarNav"]//section[@class="FLC"]//li/a/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="PrimaryContent"]/div[@id="categoryList"]//li//a/@href', response)
        terminal_urls = [ textify(t) for t in terminal_urls ]
        for url in terminal_urls:
            get_page('ehow_terminal', url)
