import feedparser
import sys
import traceback

from scrapy.conf import settings
from juicer.utils import *
from urlparse import urlparse

class RSS_Discovery(JuicerSpider):
    name = "rss_practice"
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
            url = data['blog']['url']
            netloc = urlparse(url)
            self.allowed_domains.append(netloc[1])
            r = Request(url, self.parse, None, meta = {'data' : data})
            requests.extend(r)

        return requests

    def parse(self, response):
        if ".jpg" in response.url:
            ''
            return
        hdoc = HTML(response)

        url_file = file("/home/headrun/niranjan/rss_urls_fashion_nir", "w")
        try:
            _entries = feedparser.parse(response.body)
        except:
           pass 

        if len(_entries['entries']) > 2:
            _dict = self.url_dict.get(response.meta['data']['blog']['url'], "None")
            if not _dict == "None":
                self.url_dict[response.meta['data']['blog']['url']]['rss_url'].append(response.url)
            else:
                self.url_dict[response.meta['data']['blog']['url']] = {}
                self.url_dict[response.meta['data']['blog']['url']] = response.meta['data']
                self.url_dict[response.meta['data']['blog']['url']]['rss_url'] = [response.url]
            url_file.write("%s" %(str(self.url_dict)))


        urls = hdoc.select_urls("//a/@href", response)
        head_urls = hdoc.select_urls('//head/link/@href', response)
        urls = urls + head_urls

        for url in urls:
            if "rss" or "feeds" or "feed" or "xml" or "rdf" or "atom" in url:
                yield Request(url, self.parse, response, meta = {'data' : response.meta['data']}, priority = 10)
            else:
                if not ".jpg" in url:
                    yield Request(url, self.parse, response, meta = {'data' : response.meta['data']})

