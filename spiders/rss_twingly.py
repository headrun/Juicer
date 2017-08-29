import httplib

from juicer.utils import *

COUNTRY_CODES = ["da", "fi", "no", "sv"]

class TwinglySpider(JuicerSpider):
    name = 'rss_twingly'
    start_urls = ['http://www.twingly.com/top100?lang=%s' % code for code in COUNTRY_CODES]

    db, db_name = get_cursor()

    def parse(self, response):
        got_page(self.name, response)

        hdoc = HTML(response)
        item = Item(response, HTML)
        urls = hdoc.select_urls(['//div[@class="moreinfo"]//a[@class="linktoblog"]/@href'], response)
        for url in urls:
            url = xcode(textify(url))
            if '.blogspot.' in url:
                url = url.split('/')[2]
                url = 'http://' + url + '/feeds/posts/default'
            else:
                url = url + '/feed/'
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            #print doc

            try:
                TwinglySpider.db.insert(TwinglySpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                continue
        got_page(self.name, response)
