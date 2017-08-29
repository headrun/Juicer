from juicer.utils import *

class MenuBrowseSpider(JuicerSpider):
    name = 'menu_browse'
    allow_domain = 'menupages.com'
    start_urls = 'http://www.menupages.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls('//div[@id="list-by-cuisine"]//div[@class="content"]//ul//li//a/@href',response)
        for url in urls:
            get_page(self.name, url)

        next_urls = hdoc.select_urls('//td[@class="name-address"]//a[@class="link"]/@href'\
                                     '//div[@class="pagination"]//li//a[contains(text(),"\xe2\x80\xba")]/@href', response)
        for url in next_urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls(['//td[@class="name-address"]//a[@class="link"]/@href'], response)
        for url in terminal_urls:
            get_page('menu_terminal', url)
