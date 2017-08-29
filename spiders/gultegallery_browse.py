
from juicer.utils import *

class GulteGalleryBrowseSpider(JuicerSpider):
    name = 'gultegallery_browse'
    allow_domain = 'gulte.com'
    start_urls = ['http://www.gulte.com/photos/']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a[contains(text(), "More")]/@href', '//ul[@class="pagination"]//li/a[@class="next"]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="left gallery"]//ul[@class="photoGallery thumb clearfix"]/li/a/@href', response)
        for terminal_url in terminal_urls:
            get_page('gultegallery_terminal', terminal_url)
