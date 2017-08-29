from juicer.utils import *
import re
import urllib
import hashlib
from datetime import date

class OmgiliSpider(JuicerSpider):
    name = 'omgili'

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.db, self.db_name = get_cursor()

    def parse(self, response):
        got_page(self.name, response)

        hdoc = XML(response)

        urls = hdoc.select_urls(['/XML/Results/Item/DiscussionSource'], response)
        for url in urls:
            doc = {}
            doc['last_run'] = 0
            doc['next_run'] = 0
            doc['url'] = url
            doc['url_hash'] = hashlib.md5(url).hexdigest()
            doc['forum_type'] = ''
            doc['title'] = ''
            OmgiliSpider.db.update(self.db_name, 'forum',spec={'url_hash': hashlib.md5(url).hexdigest()} , doc=doc, upsert=True)
            yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()

        for i in range(9):
            n_url = response.url
            n_url = n_url.split('=')
            n_url[-1] = str(i + 2)
            url = '='.join(n_url)
            yield Request(url, self.parse_details, None)

    def parse_details(self, response):
        hdoc = XML(response)

        urls = hdoc.select_urls(['/XML/Results/Item/DiscussionSource'], response)

        for url in urls:
            doc = {}
            doc['last_run'] = 0
            doc['next_run'] = 0
            doc['url'] = url
            doc['url_hash'] = hashlib.md5(url).hexdigest()
            doc['forum_type'] = ''
            OmgiliSpider.db.update(self.db_name, 'forum',spec={'url_hash': hashlib.md5(url).hexdigest()} , doc=doc, upsert=True)
            yield Item(response).set_many({'url': url, 'sk': md5(url)}).process()

