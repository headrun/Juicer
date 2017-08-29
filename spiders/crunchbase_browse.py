from juicer.utils import *

class SpiderCrunchBase(JuicerSpider):
    name = 'crunchbase_browse'
    start_urls = 'http://www.crunchbase.com/companies'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//a/@href[contains(., "/companies")]'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//a/@href[contains(., "/company/")]', response)
        for url in terminal_urls:
            get_page('crunchbase_terminal', url)
