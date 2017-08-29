from juicer.utils import *

class MenupagesSpider(JuicerSpider):
    name = 'menupages_browse'
    allowed_domains = ['menupages.com']
    start_urls = 'http://www.menupages.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@class="col-a"]//li//a/@href',\
                                 '//ul[@class="col-b"]//li//a/@href',\
                                 '//div[@class="pagination"]//ul//li[@class="current"]//following-sibling::li[1]//a/@href'], response)
        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//td[@class="name-address"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('?restaurantid=')[-1].split('&page=')[0]
            get_page('menupages_terminal', url, sk=sk)
