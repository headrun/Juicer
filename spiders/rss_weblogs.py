import httplib

from juicer.utils import *

class WeblogsSpider(JuicerSpider):
    name = 'rss_weblogs'
    start_urls = 'http://weblogs.com/pingservice?action=audioping'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//weblog/@changesurl', response)

        for url in urls:
            url = xcode(textify(url))
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}

            try:
                WeblogsSpider.db.insert(WeblogsSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                continue
        got_page(self.name, response)

