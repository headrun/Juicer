from juicer.utils import *

class DealnewsBrowseSpider(JuicerSpider):
    name = 'dealnews_browse'
    start_urls = ['http://dealnews.com/categories/']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//td[@valign="top"]//h2//a/@href',\
                                 '//div[@class="unit size2of3 lastUnit pager-right"]//a/@href'], response)
        for url in urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls(['//h3[@class="std-headline"]//a/@href'],response)
        for terminal_url in terminal_urls:
            get_page('dealnews_terminal', terminal_url)
