from juicer.utils import *

class DealerraterBrowseSpider(JuicerSpider):
    name = 'dealerrater_browse'
    allowed_domains = ['dealerrater.com']
    start_urls = 'http://www.dealerrater.com/directory/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="statesManus"]//table[@id="ctl00_middleContent_stateList"]//td//a/@href',\
                                 '//table[@id="ctl00_middleContent_manufacturerList"]//td//a/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//td[@style="width:112px;"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('-')[-1].split('/')[0]
            get_page('dealerrater_terminal', url)
