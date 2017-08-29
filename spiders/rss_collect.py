import feedparser
import sys
import traceback
from scrapy.conf import settings
from juicer.utils import *
from urlparse import urlparse

class RSS_Discovery(JuicerSpider):
    name = "rss_collect"
    #settings.overrides['DEPTH_LIMIT'] = 2
    settings.overrides['DEPTH_PRIORITY'] = 1
    settings.overrides['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
    settings.overrides['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
    allowed_domains = []
    input_file = '/home/headrun/venu/machine2/retry/retry/indonesia_news'
    output_file = '/home/headrun/venu/machine2/retry/retry/indonesia_news_feeds'

    def start_requests(self):
        requests = []
        _urls = []
        urls = file(self.input_file,'r')

        """url may be like feeds.feedburner, normal feed,
        boardreader.com, facebook, youtube feed"""
        for url in urls.readlines():
            li = url.replace('\n', '').split('\t')
            url = li[0]
            for i in li:
                if i.endswith('_sourcetype_manual'): _type = i

            try:
                data = urllib2.urlopen(feed_url, timeout=60).read()
            except Exception as e:
                data = None
            if not data:
                continue

            netloc = urlparse(url)
            _urls.append(url)
            self.allowed_domains.append(netloc[1])
            '''
            domain = netloc[1]
            if not domain == 'boardreader.com':
                feeds = feedparser.parse(url)
                try:
                    url = feeds.feed['link']
                    print url
                    _urls.append(url)
                except:
                    try:
                        netloc = urlparse(url)
                        url = netloc.netloc
                        url = 'http://'+url
                        _urls.apppend(url)
                    except:
                        pass
            '''

        _urls = list(set(_urls))
        for url in _urls:
            url = url.strip()
            r = Request(url, self.parse, None)
            requests.extend(r)

        print len(requests)
        print requests
        return requests

    def parse(self, response):
        try:
            hdoc = HTML(response)
            try:
                _entries = feedparser.parse(response.body)
                if len(_entries['entries']) > 1:
                    print response.url
                    out_file = file(self.output_file,'ab+')
                    out_file.write('%s\n' %(response.url))
                    out_file.close()
            except:
                pass

            urls = hdoc.select_urls("//a/@href", response)
            head_urls = hdoc.select_urls('//link/@href', response)
            urls = urls + head_urls

            for url in urls:
                rss_url = url.lower()
                if 'rss' in rss_url or 'feeds' in rss_url or 'feed' in rss_url or 'xml' in rss_url or 'rdf' in rss_url or 'atom' in rss_url:
                    yield Request(url, self.parse, response, priority = 10)
                else:
                    yield Request(url, self.parse_sub, response)
        except:
            pass

    def parse_sub(self, response):
        try:
            hdoc = HTML(response)

            urls = hdoc.select_urls("//a/@href", response)
            head_urls = hdoc.select_urls('//link/@href', response)
            urls = urls + head_urls

            for url in urls:
                rss_url = url.lower()
                if 'rss' in rss_url or 'feeds' in rss_url or 'feed' in rss_url or 'xml' in rss_url or 'rdf' in rss_url or 'atom' in rss_url:
                    yield Request(url, self.parse, response, priority = 10)
                else:
                    yield Request(url, self.parse_terminal, response)
        except:
            pass

    def parse_terminal(self, response):
        try:
            hdoc = HTML(response)

            urls = hdoc.select_urls("//a/@href", response)
            head_urls = hdoc.select_urls('//link/@href', response)
            urls = urls + head_urls

            for url in urls:
                rss_url = url.lower()
                if 'rss' in rss_url or 'feeds' in rss_url or 'feed' in rss_url or 'xml' in rss_url or 'rdf' in rss_url or 'atom' in rss_url:
                    yield Request(url, self.parse, response, priority = 10)
        except:
            pass
