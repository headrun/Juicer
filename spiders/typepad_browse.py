from juicer.utils import *

class TypepadBrowseSpider(JuicerSpider):
    name = 'typepad_browse'
    start_urls = 'http://profile.typepad.com/avatar'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="module-list pkg"]/a[@target="_parent"]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        next_urls = hdoc.select_urls(['//a[contains(text(),"Next")]/@href'], response)
        for url in next_urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="contact-name"]/a/@href'], response)
        for url in terminal_urls:
            get_page('typepad_terminal', url)
