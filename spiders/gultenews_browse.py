
from juicer.utils import *

class GulteNewsBrowseSpider(JuicerSpider):
    name = 'gultenews_browse'
    allow_domain = 'gulte.com'
    start_urls = 'http://www.gulte.com/movienews'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        next_urls = hdoc.select_urls('//ul[@class="pagination"]//a[contains(., "Next")]/@href', response)
        for url in next_urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls('//div[@class="listView"]//li//a/@href[not(contains(., "Photos"))][not(contains(., "Posters"))]', response)
        for url in terminal_urls:
            get_page('gultenews_terminal', url)

