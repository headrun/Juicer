from juicer.utils import *

class EdmundsSpider(JuicerSpider):
    name = 'edmunds_browse'
    allowed_domains = ['edmunds.com']
    start_urls = 'http://www.edmunds.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="makes_list_module"]//ul//li//a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//p[@class="name"]//a/@href', response)
        for url in terminal_urls:
            sk = url
            get_page('edmunds_terminal', url, sk=sk)
