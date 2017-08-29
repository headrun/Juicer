#! /usr/bin/env python

import httplib
from juicer.utils import *

class SpiderDisqus(JuicerSpider):
    name = 'rss_disqus'
    allowed_domains = ['http://disqus.com/']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)

        self.db, self.db_name = get_cursor()

    def start_requests(self):
        requests = []
        for counter in xrange(0, 10000, 10):
            url = "http://disqus.com/explore/?offset=%s" % str(counter)
            requests.extend(Request(url, self.parse, None, headers={'header':'X-Requested-With:XMLHttpRequest'}))
        return requests

    def parse(self, response):

        for url in re.findall('http://[^ ]*.disqus.com', response.body):
            url = '%s/latest.rss' % xcode(url)
            doc = {'url': url, 'url_hash': hashlib.md5(url).hexdigest(), 'last_run':0, 'next_run':0}
            try:
                self.db.insert(self.db_name, "rss", doc=doc)
                yield Item(response).set_many({'sk': md5(url), 'url':url}).process()
            except httplib.BadStatusLine:
                # ignoring. bug in cloudlibs db service.
                continue


