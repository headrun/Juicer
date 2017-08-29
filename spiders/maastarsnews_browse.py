
from juicer.utils import *

class MaaStarsNewsBrowseSpider(JuicerSpider):
    name = 'maastarsnews_browse'
    allow_domain = 'maastars.com'
    start_urls = ['http://www.maastars.com/category/news/news-happenings' ,'http://www.maastars.com/category/news/tollywood-gossips', 'http://www.maastars.com/category/news/popcorn']


    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        next_urls = hdoc.select_urls('//div[@class="nav-previous"]/a/@href', response)
        for url in next_urls:
            get_page(self.name, url)


        terminal_urls = hdoc.select_urls('//div[@class="list"]//li/a/@href', response)
        for url in terminal_urls:
            get_page('maastarsnews_terminal', url)

