import httplib

from juicer.utils import *

class KpingSpider(JuicerSpider):
    name = 'rss_kping'
    start_urls = 'http://www.kping.com/rssfeeds/'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//li[@class="recentping"]//a//img//parent::a/@href'], response)

        for url in urls:
            url = xcode(textify(url))
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}

            try:
                KpingSpider.db.insert(KpingSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                continue
        got_page(self.name, response)
