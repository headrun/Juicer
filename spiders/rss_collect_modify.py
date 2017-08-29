import feedparser
import sys
import traceback
from scrapy.conf import settings
from juicer.utils import *
from urlparse import urlparse

class RSS_Discovery(JuicerSpider):
    name = "rss_collect_modify"
    #settings.overrides['DEPTH_LIMIT'] = 2
    settings.overrides['DEPTH_PRIORITY'] = 1
    settings.overrides['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
    settings.overrides['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
    allowed_domains = []
    input_file = '/home/headrun/venu/machine2/china_news'
    output_file = '/home/headrun/venu/machine2/consumercourt'

    '''
    def start_requests(self):

        requests = []
        _urls = []
        urls = file(self.input_file,'r').readlines()

        for url in urls:
            url = url.split('\t')[0]
            netloc = urlparse(url)
            self.allowed_domains.append(netloc[1])
            domain = netloc[1]
            if not domain == 'scubaboard.com' and not domain == 'dumagueteinfo.com':
                try:
                    feeds = feedparser.parse(url)
                    url = feeds.feed['link']
                    print url
                    _urls.append(url)
                except:
                    pass

        _urls = list(set(_urls))
        for url in _urls:
            r = Request(url, self.parse, None)
            requests.extend(r)

        print len(requests)
        return requests
    '''
    def start_requests(self):

        requests = []
        urls = ['http://www.consumercourt.in/']
        for url in urls:
            url = url.split('\t')[0]
            netloc = urlparse(url)
            self.allowed_domains.append(netloc[1])
            r = Request(url, self.parse, None)
            requests.extend(r)

        print len(requests)
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
        except:
            pass

