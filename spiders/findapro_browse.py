from juicer.utils import *

class FindaproSpider(JuicerSpider):
    name = 'findapro_browse'
    allowed_domains = ['findapro.com']
    start_urls = 'http://www.findapro.com/directory'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//span//parent::a[@id][@rel]/@href',\
                                 '//ul[@class="cities"]//table//td//a/@href'], response)

        for url in urls: get_page(self.name, url)

        next_url = hdoc.select_urls('//span[@class="next"]//parent::a/@href', response)
        if next_url:
            next_url = next_url[0]

            get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls(['//div[@class="name"]//a/@href'], response)

        for url in terminal_urls: get_page('findapro_terminal', url)
