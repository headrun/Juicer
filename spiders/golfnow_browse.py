from juicer.utils import *

class GolfNowBrowseSpider(JuicerSpider):
    name = 'golfnow_browse'
    allow_domain = ['golfnow.com']
    start_urls = ['http://www.golfnow.com/']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//li[@class=" navFirst"]//a/@href','//ul[@class="stateList"]//a/@href','//ul[@class="metroList"]//li/a/@href' \
                                 '//ul[@class="cityList"]//li/a/@href'],response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//ul[@class="courseList"]//li/a/@href'], response)
        for url in terminal_urls:
            get_page('golfnow_terminal', url)
