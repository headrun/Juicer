from juicer.utils import *

class PlurkBrowseSpider(JuicerSpider):
    name = 'plurk_browse'
    start_urls = 'http://www.plurk.com/Verified/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@id="section_list"]//li//a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//td[@class="u_content"]//a/@href'], response)
        for url in terminal_urls:
            get_page('plurk_terminal', url)
