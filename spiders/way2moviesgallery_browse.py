
from juicer.utils import *

class Way2MoviesGalleryBrowseSpider(JuicerSpider):
    name = 'way2moviesgallery_browse'
    allow_domain = 'way2movies.com'
    start_urls = ['http://telugu.way2movies.com/gallery_telugu/5.html', 'http://hindi.way2movies.com/gallery_hindi/5.html', 'http://tamil.way2movies.com/gallery_tamil/5.html']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="tabs1 pos-rel"]//li/a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        next_urls = hdoc.select_urls('//div[@class="navigation"]//a[contains(.,"next")]/@href',response)
        for next_url in next_urls:
            get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls('//div[@class="photo_table"]//a[@class="gallery_title"]/@href', response)
        for terminal_url in terminal_urls:
            get_page('way2moviesgallery_terminal', terminal_url)

