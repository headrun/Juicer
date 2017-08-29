from juicer.utils import *

class BlogCatalogBrowseSpider(JuicerSpider):
    name = 'blogcatalog_browse'
    start_urls = 'http://www.blogcatalog.com/bloggers/city'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="margin_bottom_20"]//p//a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        next_url = hdoc.select_urls(['//div[@class="pagination"]//a[contains(text(), "NEXT")]/@href'], response)
        for url in next_url:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="details"]//h3//a/@href'], response)
        for terminal_url in terminal_urls:
            get_page('blogcatalog_terminal', terminal_url)
