import feedparser
import sys
import traceback
import logging
log = logging.getLogger()

from scrapy.conf import settings
from juicer.utils import *
from urlparse import urlparse


class RSS_Discovery(JuicerSpider):
    name = "rss_dis_1"
    #settings.overrides['DEPTH_LIMIT'] = 4
    allowed_domains = []

    def start_requests(self):
        cur,db_name = get_cursor()
        cutoff_time = int(time.time()) - 6 * 86400
        results = cur.find('juicerprod', 'rss_sources', limit =100, spec = {'dt_last_crawl':{'$lte': cutoff_time}})
        requests = []
        count = {}

        for result in results['result']:
            url = result['base_url']
            _id = result['_id']
            count[result['_id']] = 0
            netloc = urlparse(url)
            p.update("juicerprod" , "rss_sources" , specs = {'_id': _id } , document = {'dt_last_crawl': int(time.time())})
            self.allowed_domains.append(netloc[1])
            r = Request(url, self.parse, None, meta={'_id': _id, 'count' : count})
            requests.extend(r)

        return requests

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.count = {}
        self.time = int(time.time())
        if kwargs.get("PATH"):
            self.path = kwargs.get("PATH")

    def parse(self, response):
        hdoc = HTML(response)

        if self.path:
            data = file("%srss_urls_%s.unprocessed" %(self.path,self.time), "ab+")
        else:
            data = file("/tmp/rss_urls_%s" %(self.time), "ab+")

        count = response.meta['count']
        count[response.meta['_id']] = count[response.meta['_id']] + 1
        print "count >>>",count[response.meta['_id']]

        try:
            _entries = feedparser.parse(response.body)
            if len(_entries['entries']) > 2:
                data.write("%s\t%s\n" %(response.url, response.meta['_id']))
                return
        except:
            #print ''.join(traceback.format_exception(*sys.exc_info()[:3]))
            pass

        urls = hdoc.select_urls("//a/@href", response)
        if count[response.meta['_id']] < 1000:
            for url in urls:
                if "rss" or "feeds" or "feed" or "xml" or "rdf" or "atom" in url:
                    yield Request(url, self.parse, response, meta = {'_id': response.meta['_id'], 'count' : count }, priority = 10)
                else:
                    yield Request(url, self.parse, response, meta = {'_id': response.meta['_id'], 'count' : count})

