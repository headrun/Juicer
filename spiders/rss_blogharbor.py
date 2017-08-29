import httplib

from juicer.utils import *

class BlogharborSpider(JuicerSpider):
    name = 'rss_blogharbor'
    start_urls = 'http://www.blogharbor.com/cgi-bin/page.cgi?page=/recently_updated.html'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//div[@class="main"]//table//td[@style]//a/@href'], response)

        for url in urls:
            url = xcode(textify(url))
            url = url + '/blog/index.xml'
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}

            try:
                BlogharborSpider.db.insert(BlogharborSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                continue
        got_page(self.name, response)
