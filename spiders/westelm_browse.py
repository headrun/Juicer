from juicer.utils import *

class WestelmBrowseSpider(JuicerSpider):
    name = 'westelm_browse'
    allowed_domains = ['westelm.com']
    start_urls = 'http://www.westelm.com/sitemap.html?cm_type=fnav'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="cols"]//ul//li//a/@href', '//a[contains(text(),"Next")]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//ul[@class="product-list"]//li//a/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-2].split('-')[-1]
            get_page('westelm_terminal', url)
