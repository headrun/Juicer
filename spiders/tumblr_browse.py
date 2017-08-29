from juicer.utils import *

class TumblrBrowseSpider(JuicerSpider):
    name = 'tumblr_browse'
    start_urls = 'http://www.tumblr.com/explore'
    limit_start_urls = 2000

    def parse(self, response):
        got_page(self.name, response)

        hdoc = HTML(response)

        for url in hdoc.select_urls('//@href[contains(., "/tagged/")]', response):
            url =url
            get_page(self.name, url)

        for url in hdoc.select_urls('//@href[contains(., "/everything")]', response):
            url = url
            get_page(self.name, url)

        for url in hdoc.select_urls('//a[@class="blog"]/@href', response):
            url = url
            get_page(self.name, url)

        for url in hdoc.select_urls('//div[@id="pagination"]//a[contains(text(),"Next")]/@href', response):
            url = url
            get_page(self.name, url)

        '''for url in hdoc.select_urls('//@href[contains(., "/tagged/")]', '//@href[contains(., "/everything")]', '//a[@class="blog"]/@href', '//div[@id="pagination"]//a[contains(text(),"Next")]/@href', response):
            get_page(self.name, url)'''

        for url in hdoc.select_urls('//div[@class="post_info"]//a/@href', response):
            get_page('tumblr_terminal', url)
