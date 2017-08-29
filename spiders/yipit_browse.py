from juicer.utils import *

class YipitSpider(JuicerSpider):
    name = 'yipit_browse'
    allowed_domains = ['yipit.com']
    start_urls = 'http://yipit.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="footer-menu"]//h5[contains(text(),"Deals")]//following-sibling::ul//li//a/@href',\
                                 '//div[@class="pagination"]//a/@href'], response)

        for url in urls:
            get_page(self.name, url)

        '''next_urls = hdoc.select_urls(['//div[@class="pagination"]//a/@href'], response)
        for url in next_urls:
            get_page(self.name, url)
        '''

        terminal_urls = hdoc.select_urls('//ol[@class="numbered_list"]//li//a/@href', response)
        for url in terminal_urls:
            get_page('yipit_terminal', url)
