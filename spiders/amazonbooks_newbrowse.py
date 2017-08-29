from juicer.utils import *

class AmazonBooksNewSpider(JuicerSpider):
    name = 'amazonbooks_newbrowse'
    allowed_domains = ['amazon.com']
    start_urls = 'http://www.amazon.com/gp/search/other?redirect=true&rh=n:283155&bbn=283155&pickerToList=lbr_one_browse-bin&ie=UTF8&qid=1317796036&rd=1'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//span[@class="refinementLink"]//parent::a/@href',\
                                 '//ul[@data-typeid="n"]//li//a/@href',\
                                 '//ul[@data-typeid="n"]//li//a/@href[not(contains(., "=sr_ex"))]',\
                                 '//a[contains(text(), "Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="title"]//a[@class="title"]/@href'])

        for url in terminal_urls: get_page('amazonbooks_newterminal', url)
