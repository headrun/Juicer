import httplib

from juicer.utils import *

class BloggerSpider(JuicerSpider):
    name = 'rss_blogger'
    start_urls = 'http://www.blogger.com/changes10.g'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//ol//li//a/@href'], response)

        for url in urls:
            url = xcode(textify(url))
            url = url + '/feeds/posts/default?alt=rss'
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            try:
                BloggerSpider.db.insert(BloggerSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                #print 'BadStatusLine error'
                continue
