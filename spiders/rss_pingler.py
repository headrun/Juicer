import httplib

from juicer.utils import *

class PinglerSpider(JuicerSpider):
    name = 'rss_pingler'
    start_urls = 'http://pingler.com/categories.php'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//div[@id="catList"]//a/@href', response)
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//div[contains(@style,"padding")]//a[1][@rel="nofollow"]/@href', response)
        for url in urls:
            url = xcode(textify(url))
            url = url + '/feed/'
            print url
            yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()

        got_page(self.name, response)
