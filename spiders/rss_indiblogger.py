import feedparser
import sys
import traceback

from scrapy.conf import settings
from juicer.utils import *
from urlparse import urlparse

class RSS_Discovery(JuicerSpider):
    name = "rss_indiblogger_01"
    #settings.overrides['DEPTH_LIMIT'] = 4
    settings.overrides['DEPTH_PRIORITY'] = 1
    settings.overrides['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
    settings.overrides['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
    allowed_domains = []
    url_dict = {}

    def start_requests(self):
        requests = []
        urls = file('indiblogger_text', 'r').readlines()
        for i in urls:
            data = eval(i)
            _url = data['blog']['url']
            #etloc = urlparse(url)
            #elf.allowed_domains.append(netloc[1])
            r = Request(_url, self.parse, None, meta = {'data' : data, 'url_dict': self.url_dict})
            requests.extend(r)

        return requests

    def parse(self, response):
        hdoc = HTML(response)
        print response.url

        data = file("/home/headrun/niranjan/rss_urls_fashion_1", "w+")
        try:
            if not ".jpg" or not '.ico' in response.url:
                _entries = feedparser.parse(response.body)
                if len(_entries['entries']) > 2:
                    meta_data = response.meta['data']
                    _url = meta_data['blog']['url']
                    if self.url_dict[_url]:
                        self.url_dict[response.meta['url']].append(response.url)
                    else:
                        self.url_dict[response.meta['url']]=[]
                        self.url_dict[response.meta['url']].append(response.url)
                    import pdb;pdb.set_trace()
                    #data.write("%s" %(response.url))
                    data.close()
                    print 'feed_url>>>>>', response.url, response.meta['data']
                    return
        except:
            pass

        urls = hdoc.select_urls("//a/@href", response)
        head_urls = hdoc.select_urls('//head/link/@href', response)
        urls = urls + head_urls

        for url in urls:
            if "rss" or "feeds" or "feed" or "xml" or "rdf" or "atom" in url:
                yield Request(url, self.parse, response, meta = {'data' : response.meta['data']}, priority = 10)
            else:
                if not ".jpg" in url:
                    yield Request(url, self.parse, response, meta = {'data' : response.meta['data']})

