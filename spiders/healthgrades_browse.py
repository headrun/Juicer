from juicer.utils import *

class HealthgradesSpider(JuicerSpider):
    name = 'healthgrades_browse'
    allowed_domains = ['healthgrades.com']
    start_urls = 'http://www.healthgrades.com/sitemap/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//@href[contains(., "/affiliated-physicians/")]', \
                                 '//a[contains(text(), "Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//tr[@valign="top"]//ul//li//a/@href'], response)

        for url in terminal_urls: get_page('healthgrades_terminal', url)
