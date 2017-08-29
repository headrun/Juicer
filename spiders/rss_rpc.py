import httplib

from juicer.utils import *

class RpcSpider(JuicerSpider):
    name = 'rss_rpc'
    start_urls =['http://rpc.weblogs.com/shortChanges.xml']

    db, db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)
        urls = hdoc.select_urls(['//weblog/@url'], response)
        #print '0000000000000000000', len(urls)

        for url in urls:
            url = xcode(textify(url))
            print ">>>>>>>>>>>>", url
            get_page(self.name, url)
            doc = {'url': url, 'url_hash': md5(url), 'last_run':0, 'next_run': 0}
            #yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()

            try:
                RpcSpider.db.insert(RpcSpider.db_name, "rss", doc=doc)
                yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()
            except httplib.BadStatusLine:
                print 'BadStatusLine error'
                continue
        #yield item.process()
        #got_page(self.name, response)
