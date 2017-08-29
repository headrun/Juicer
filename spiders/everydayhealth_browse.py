from juicer.utils import *

class EverydayhealthSpider(JuicerSpider):
    name = 'everydayhealth_browse'
    allowed_domains = ['everydayhealth.com']
    start_urls = 'http://www.everydayhealth.com/doctors'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//h3[contains(text(), "Doctor Directory by Name:")]//parent::div[@class="inner"]//ul//li//a/@href',\
                                 '//div[@class="result"]//a[contains(text(),"Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="columns"]//div//ul//li//a/@href'], response)

        for url in terminal_urls: get_page('everydayhealth_terminal', url)
