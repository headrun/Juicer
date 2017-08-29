from juicer.utils import *

class AllmenusSpider(JuicerSpider):
    name = 'allmenus_browse'
    allowed_domains = ['allmenus.com']
    start_urls = 'http://www.allmenus.com/welcome/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls('//ul[@class="states"][2]//li//a/@href', response)
        print "urls:",urls
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="grid_8 push_2"]//ul//li//a/@href', response)
        print "terminal:",terminal_urls
        for url in terminal_urls:
            get_page('allmenus_terminal', url)
