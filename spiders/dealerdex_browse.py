from juicer.utils import *

class DealerdexSpider(JuicerSpider):
    name = 'dealerdex_browse'
    allowed_domains = ['dealerdex.com']
    start_urls = 'http://www.dealerdex.com/Default.aspx'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//h2[contains(text(), "Find Used Car Dealers in Your State")]//parent::div[@class="blogmid"]//div//a/@href',\
                                 '//table[@class="makebystatetbl"]//tr//td//a/@href'], response)

        for url in urls: get_page(self.name, url)

        #terminal_urls = hdoc.select_urls(['//@href[contains(., "/DealerInfo.aspx/")]'], response)
        terminal_urls = hdoc.select_urls(['//table[@class="searchlisttable"]//td//a/@href'], response)

        for url in terminal_urls: get_page('dealerdex_terminal', url)
