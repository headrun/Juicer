from juicer.utils import *

class Amazonapps1BrowseSpider(JuicerSpider):
    name = 'amazonapps_browse'
    allowed_domains = ['amazon.com']
    start_urls = 'http://www.amazon.com/mobile-apps/b/ref=sa_menu_adr_app4?ie=UTF8&node=2350149011'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[contains(text(),"Categories")]//following-sibling::ul//li//a/@href', '//a[contains(text(),"Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="productTitle"]//a/@href', response)

        for url in terminal_urls: get_page('amazonapps_terminal', url)
