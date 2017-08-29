from juicer.utils import *

class HolidayrentalsSpider(JuicerSpider):
    name = 'holidayrentals_browse'
    allowed_domains = ['holiday-rentals.co']
    start_urls = 'http://www.holiday-rentals.co.uk/World/r1.htm'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="pager"]//a[contains(text(),"Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//h3[@class="listing-title"]//a/@href'], response)

        for url in terminal_urls:
            sk = url.split('/')[-1]
            get_page('holidayrentals_terminal', url, sk=sk)
