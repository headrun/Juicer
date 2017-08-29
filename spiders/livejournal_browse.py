from juicer.utils import *

class LivejournalBrowseSpider(JuicerSpider):
    name = 'livejournal_browse'
    start_urls = 'http://www.livejournal.com/browse/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@class="m-section"]//span//a/@href', '//a[@title="Next"]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        for url in  hdoc.select_urls('//span[@class="ljuser ljuser-name_"]//a[1]/@href', response):
            get_page('livejournal_terminal', url)

