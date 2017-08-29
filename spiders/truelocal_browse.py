from juicer.utils import *

class TruelocalBrowseSpider(JuicerSpider):
    name = 'truelocal_browse'
    allowed_domains = ['truelocal.com.au']
    start_urls ='http://www.truelocal.com.au/business-type' 

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//div[@class="browse-list clearfix"]//li//a/@href',\
                                 '//a[contains(text(),"Next")]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="TL_search_results_list"]//a[@class="org"]/@href'], response)
        for url in terminal_urls:
            get_page('truelocal_terminal', url)
