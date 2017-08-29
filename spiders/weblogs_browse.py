from juicer.utils import *

class WeblogsSpider(JuicerSpider):
    name = 'weblogs_browse'
    allowed_domains = ['weblogs.com.ph']
    start_urls = 'http://weblogs.com.ph/tags/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="content-full"]//a/@href[contains(., "/tags/letter-")]',\
                                 '//div[@class="content-full"]//a/@href[contains(., "/view")]'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="content-full"]//td//b//a/@href'], response)

        for url in terminal_urls: get_page('weblogs_terminal', url)
