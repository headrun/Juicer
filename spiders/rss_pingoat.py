import httplib

from juicer.utils import *

class PingoatSpider(JuicerSpider):
    name = 'rss_pingoat'
    start_urls = ['http://recent.pingoat.com/']

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//div[@class="list_url"]//a/@href', response)
        #print '0000000000000000000', len(urls)

        for url in urls:
            url = xcode(textify(url))
            print ">>>>>>>>>>>>", url 
            get_page(self.name, url)
            yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()

        got_page(self.name, response)
