from juicer.utils import *

class PurelandsupplySpider(JuicerSpider):
    name = 'purelandsupply_browse'
    allowed_domains = ['purelandsupply.com']
    start_urls = 'http://www.purelandsupply.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="leftmenu"]//a/@href',\
                                 '//img[@alt="Move Next"]//parent::a//@href[1]'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@id="Img"]//a/@href', response)
        for url in terminal_urls:
            get_page('purelandsupply_terminal', url)
