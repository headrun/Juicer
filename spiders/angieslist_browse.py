from juicer.utils import *

class AngieslistSpider(JuicerSpider):
    name = 'angieslist_browse'
    allowed_domains = ['angieslist.com']
    start_urls = 'http://www.angieslist.com/companylist/us/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//table[@class="itemlist"]//td//a/@href'], response)

        for url in urls: get_page(self.name, url)

        next_urls = hdoc.select_urls(['//div[@id="spnav"]//img[@alt="Next"]//parent::a/@href'], response)

        for url in next_urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="name"]//a/@href'], response)

        for url in terminal_urls: get_page('angieslist_terminal', url)
