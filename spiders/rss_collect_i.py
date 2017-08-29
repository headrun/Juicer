import feedparser
import sys
import traceback
from scrapy.conf import settings
from juicer.utils import *
from urlparse import urlparse

class RSS_Discovery(JuicerSpider):
    name = "rss_collect_i"
    #settings.overrides['DEPTH_LIMIT'] = 2
    settings.overrides['DEPTH_PRIORITY'] = 1
    settings.overrides['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
    settings.overrides['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
    allowed_domains = ["feeds.feedburner.com"]

    output_file = '/home/headrun/venu/rss/usa_rss'

    def start_requests(self):
        requests = []
        conn = MySQLdb.connect('localhost','root','root','RSS_SOURCES')
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        sql = "SELECT url,netloc FROM rss_sources WHERE country= '%s' AND is_crawled=0 limit 10" %("usa")
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            my_list = []
            for row in results:
                url = row[0]
                my_list.append(str(url))
                netloc = row[1]
                self.allowed_domains.append(netloc)

                r = Request(url, self.parse, None)
                requests.extend(r)

            my_tuple = tuple(my_list)
            try:
                query = "UPDATE rss_sources SET is_crawled = 2 WHERE url in %s"
                values = str((my_tuple))
                cursor.execute(query % values)
            except: print "error in updating status as 2"

        except: print "error in forming requests"

        print len(requests)
        return requests

    def parse(self, response):
        try:
            hdoc = HTML(response)
            try:
                _entries = feedparser.parse(response.body)
                if "feeds.feedburner.com" in response.url:
                    link = _entries.get("feed", {}).get("link","")
                    netloc = urlparse(link).netloc
                    if netloc not in self.allowed_domains:
                        raise
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

