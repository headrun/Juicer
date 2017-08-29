from juicer.utils import *

class PinterestSpider(JuicerSpider):
    name = 'pinterest_browse'
    allowed_domains = ['pinterest.com']
    start_urls = ['http://pinterest.com/search/people/?q=Ieva+Mazeikaite']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        terminal_urls = hdoc.select_urls(['//div[@class="pin user"]//a/@href'], response)
        for url in terminal_urls: get_page('pinterest_terminal', url)
