from juicer.utils import *

class BoatTraderBrowseSpider(JuicerSpider):
    name = 'boattrader_browse'
    allowed_domains = ['http://www.boattrader.com']
    start_urls = 'http://www.boattrader.com/browse/state'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//div[@class="browseLocationColumn"]//a/@href',\
                                 '//div[@class="resultsPag"]//a[contains(@title,"Next Page")]/@href[1]'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="sBxJ"]//a/@href', response)

        for url in terminal_urls:
            get_page('boattrader_terminal', url)
