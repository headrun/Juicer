from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls(name):
    items = lookup_items('ladyfootlocker_browse', 'got_page:False', limit=100)
    if not items:
        items = [(None, None, 'http://www.ladyfootlocker.com/sitemap/')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data


class LadyfootlockerBrowseSpider(JuicerSpider):
    name = 'ladyfootlocker_browse'
    allowed_domains = ['ladyfootlocker.com']
    start_urls = gen_start_urls(name)

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = hashlib.md5(response.url).hexdigest()
        item.set('sk', sk) 
        item.set('got_page', True)
        item.set('url', response.url)
        item.update_mode = 'custom'
        yield item.process()
        urls = [ 
            hdoc.select('//li[@class="sub_item"]//a/@href'),
            hdoc.select('//a[contains(text(),"Next")]/@href'),
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(response.url, u) for u in urls]
        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk) 
            item.set('url', url)
            item.set('got_page', False)
            item.update_mode = 'custom'
            yield item.process()

        nodes = hdoc.select('//ul//li//a[@class="quickviewEnabled"]/@href')
        for node in nodes:
            url = textify(node)
            item = Item(response, HTML)
            item.set('sk', url.split('model--')[1].split('/')[0])
            item.set('url', urljoin(response.url, url))
            item.set('got_page', False)
            item.spider = 'ladyfootlocker_terminal'
            item.update_mode = 'custom'
            yield item.process()

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and old_data['got_page'] == True:
            return old_data

        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

SPIDER = LadyfootlockerBrowseSpider()

