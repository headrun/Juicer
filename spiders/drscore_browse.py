from juicer.utils import *

class DrscoreSpider(JuicerSpider):
    name = 'drscore_browse'
    allowed_domains = ['drscore.com']
    start_urls = 'http://www.drscore.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//@href[contains(., ".cfm?w=")]'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//td[@class="state"]//p//a/@href'], response)

        for url in terminal_urls: get_page('drscore_terminal', url)
