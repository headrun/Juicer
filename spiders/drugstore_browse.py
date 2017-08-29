from juicer.utils import *

class DrugstoreSpider(JuicerSpider):
    name = 'drugstore_browse'
    allowed_domains = ['www.drugstore.com/']
    start_urls = 'http://www.drugstore.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="webstoremenu"]//ul//li//a[not(contains(text(),"the sale"))]/@href',\
                                 '//div[@class="dimension"][contains(text(), "category")]//following-sibling::a[not(contains(text(), "$"))]/@href'], response)

        for url in urls: get_page(self.name, url)

        next_urls = hdoc.select_urls(['//img[@src="/img/search/search_arrow_next_on.gif"]//parent::a/@href'], response)

        for url in next_urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//span[@class="description"]//a/@href', response)

        for url in terminal_urls: get_page('drugstore_terminal', url)
