from juicer.utils import *

class OpenlibrarySpider(JuicerSpider):
    name = 'openlibrary_browse'
    allowed_domains = ['openlibrary.org']
    start_urls = 'http://openlibrary.org/subjects/accessible_book'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//span[@class="count"]//a[contains(text(), "Accessible book")]/@href',\
                                 '//h3[@class="booktitle"]//a/@href',\
                                 '//a[contains(text(), "Next")]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="title"]//a/@href'], response)

        for url in terminal_urls: get_page('openlibrary_terminal', url)
