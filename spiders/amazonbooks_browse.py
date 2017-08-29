from juicer.utils import *

class AmazonBooksSpider(JuicerSpider):
    name = 'amazonbooks_browse'
    allowed_domains = ['amazon.com']
    start_urls = 'http://www.amazon.com/best-sellers-books-Amazon/zgbs/books'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="zg_tabs"]//li[@class]//div//a/@href',\
                                 '//ul[@id="zg_browseRoot"]/ul/li/a/@href',\
                                 '//ul[@id="zg_browseRoot"]/ul/ul/li/a/@href',\
                                 '//ul[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href',\
                                 '//ul[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/@href',\
                                 '//label[contains(text(),"Year:")]//parent::ol//li//a/@href',\
                                 '//label[contains(text(),"Month:")]//parent::ol//li//a/@href',\
                                 '//label[contains(text(),"Weeks")]//parent::ol//li//a/@href',\
                                 '//ol[@class="zg_pagination"]//li//a/@href'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="zg_title"]//a/@href', response)
        for url in terminal_urls:
            get_page('amazonbooks_terminal', url)
