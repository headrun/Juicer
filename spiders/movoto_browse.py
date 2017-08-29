from juicer.utils import *

class MovotoSpider(JuicerSpider):
    name = 'movoto_browse'
    allowed_domains = ['movoto.com']
    start_urls = 'http://www.movoto.com'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="ctl_main_countyList"]//td//a/@href',\
                                 '//div[@class="floatRight"]//a[contains(text(),"Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="floatPropertyList"]//a[1]/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-1].split('.htm')[0]
            get_page('movoto_terminal', url, sk=sk)
