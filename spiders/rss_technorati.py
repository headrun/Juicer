from urlparse import urljoin
from itertools import chain
import hashlib
import httplib

#import feedfinder

from juicer.utils import *

class TechnoratiSpider(JuicerSpider):
    name = 'rss_technorati'
    start_urls =['http://technorati.com/blogs/directory/overall/']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.db, self.db_name = get_cursor()

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls('//a[@class="next"]/@href', response)

        for url in urls:
            yield Item(response).set_many({'sk':md5(url), 'url':url, 'got_page':False}).process()
            yield Request(url, self.parse, response)

        nodes = hdoc.select('//td[@class="site-details"]/a[@class="offsite"]/@href')
        for node in nodes:
            #url = textify(node).split('/blogs/')[-1]
            url = textify(node)

            feeds = feedfinder.feeds(xcode(url))
            for feed in feeds:
                doc = {'url': xcode(feed), 'url_hash': md5(feed), 'last_run': 0, 'next_run': 0}
                try:
                    self.db.insert(self.db_name, "rss", doc=doc)
                    yield Item(response).set_many({'sk': md5(feed), 'url': feed}).process()
                except httplib.BadStatusLine:
                    print 'got bad status line exception. ignoring.'
                    continue
                #print doc


