import httplib

from juicer.utils import *

class PingatesSpider(JuicerSpider):
    name = 'rss_pingates'
    start_urls = 'http://pingates.com/latest.php'

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        urls = hdoc.select_urls('//li[@class="messagebox"]//a/@href', response)
        #print '0000000000000000000', len(urls)

        for url in urls:
            url = url.split('/')[:3]
            url = '/'.join(url)
            url = xcode(textify(url))
            if 'blogspot.com' in url:
                url = url + '/feeds/posts/default?alt=rss'
            else:
                url = url + '/feed/'
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            try:
                PingatesSpider.db.insert(PingatesSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                #print 'BadStatusLine error'
                continue
        got_page(self.name, response)
