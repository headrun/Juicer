import feedparser
import sys
import traceback
import MySQLdb

from scrapy.conf import settings
from juicer.utils import *
from urlparse import urlparse

class RSS_Discovery(JuicerSpider):
    name = "rss_practice_a"
    #settings.overrides['DEPTH_LIMIT'] = 4
    settings.overrides['DEPTH_PRIORITY'] = 1
    settings.overrides['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
    settings.overrides['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
    allowed_domains = []

    def start_requests(self):

        requests = []
        conn = MySQLdb.connect(host='127.0.0.1', user='root', db='rss_feeds', passwd='root')
        urls_cursor = conn.cursor()
        query = 'select * from feeds where is_crawled=2'
        urls_cursor.execute(query)
        blog_urls = urls_cursor.fetchall()
        for blog_url in blog_urls:
            url = ''.join(blog_url[1])
            netloc = urlparse(url)
            self.allowed_domains.append(netloc[1])
            upt = 'UPDATE feeds SET is_crawled=2 where url="%s"' %(url)
            urls_cursor.execute(upt)
            try:
                r = Request(url, self.parse, None, meta = {'url' : url})
            except:
                pass
            requests.extend(r)

        print len(requests)
        return requests

    def parse(self, response):
        if ".jpg" in response.url:
            ''
            return
        hdoc = HTML(response)
        blog_url = response.meta['url']
        db = MySQLdb.connect("127.0.0.1","root","root","rss_feeds")
        upt_cursor = db.cursor()

        try:
            _entries = feedparser.parse(response.body)
        except:
           pass

        if len(_entries['entries']) > 2:
            query = "INSERT INTO feed_urls(url, rss_url) values"
            values = str((blog_url,response.url))
            sql = query+values
            upt_cursor.execute(sql)

            update = 'UPDATE feeds SET is_crawled = 1 where url="%s"' %(blog_url)
            upt_cursor.execute(update)
            print 'url>>>>>', response.meta['url']
            print 'feed_url>>>', response.url

        urls = hdoc.select_urls("//a/@href", response)
        head_urls = hdoc.select_urls('//head/link[@rel="alternate"]/@href', response)
        urls = urls + head_urls

        for url in urls:
            if "rss" or "feeds" or "feed" or "xml" or "rdf" or "atom" in url:
                yield Request(url, self.parse, response, meta = {'url' : response.meta['url']}, priority = 10)

