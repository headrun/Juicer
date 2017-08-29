
from juicer.utils import *

class MusicMazaaNewsBrowseSpider(JuicerSpider):
    name = 'musicmazaanews_browse'
    allow_domain = 'musicmazaa.com'
    start_urls = 'http://musicmazaa.com/news/i/entertainment-news/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        next_urls = hdoc.select_urls('//div//p[@class="pagination"]//a[contains(., "next")]//@href', response)
        for url in next_urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls('//div[@class="newsTitle"]/h2/a/@href', response)
        for url in terminal_urls:
            get_page('musicmazaanews_terminal', url)

