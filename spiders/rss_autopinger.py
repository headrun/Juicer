import httplib

from juicer.utils import *

class AutopingerSpider(JuicerSpider):
    name = 'rss_autopinger'
    start_urls = 'http://autopinger.com/recent/'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        for node in hdoc.select('//td[@align="center"]//a/@href'):
            url = xcode(textify(node))
            print url
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            #print doc
            try:
                AutopingerSpider.db.insert(AutopingerSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                print 'BadStatusLine error'
                continue
