from juicer.utils import *

class ChitramalaNewsBrowseSpider(JuicerSpider):
    name = 'chitramalanews_browse'
    allow_domain = 'chitramala.in'
    start_urls = 'http://www.chitramala.in/news/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        next_urls = hdoc.select_urls('//div[@class="navigation"]//a/@href', response)
        for url in next_urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls('//div//h2[@class="bluTitle1"]/a/@href', response)
        for url in terminal_urls:
            get_page('chitramalanews_terminal', url)

