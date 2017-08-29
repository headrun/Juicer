from juicer.utils import *

class ImdbSpider(JuicerSpider):
    name = 'imdb_browse'
    allowed_domains = ['imdb.com']
    start_urls = 'http://www.imdb.com/genre'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a[contains(@href, "/genre/")]/@href',\
                                 '//div[@class="article"]//div[@class="see-more"]//a/@href'], response)

        for url in urls: get_page(self.name, url)

        next_urls = textify(hdoc.select_urls(['//span[@class="pagination"]//a/@href'], response)).split('\n')[0]

        for url in next_urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//td[@class="title"]//a/@href[contains(., "/title/")][not(contains(., "/vote"))]'], response)

        for url in terminal_urls: get_page('imdb_terminal', url)
