from juicer.utils import *

class TaggleBrowseSpider(JuicerSpider):
    name = 'taggle_browse'
    allowed_domains = ['taggle.com']
    start_urls = 'http://www.taggle.com/browse/c/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="inner"]//ul//li//a/@href', '//a[contains(text(),"next")]//@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="heading"]//a[@class="cl"]/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-2]
            get_page('taggle_terminal', url)
