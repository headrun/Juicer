from juicer.utils import *

class BuzzillionsSpider(JuicerSpider):
    name = 'buzzillions_browse'
    allowed_domains = ['buzzillions.com']
    start_urls = 'http://www.buzzillions.com/all-product-reviews'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="bz-dept-LinksChildrenAndGrandchidren"]//p//a/@href',\
                                 '//div[@id="bz-pagination-bottom-page"]//a[contains(text(),"Next")]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="bz-model-name"]//h2//a/@href', response)
        for url in terminal_urls:
            get_page('buzzillions_terminal', url)
