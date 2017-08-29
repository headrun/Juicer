from juicer.utils import *
from itertools import chain
from urlparse import urljoin
import hashlib

def gen_start_urls():
    items = lookup_items('amazon_browse', 'got_page:False', limit=100)
    if not items:
        items = [(None, None, 'http://www.amazon.com')]
    for _id, term, data in items:
        yield data

def get_sk(url):
    split_url = url.split('/')
    sk = None
    if '/product/' in url:
        sk = split_url[split_url.index('product') + 1]
    elif '/dp/' in url:
        sk = split_url[split_url.index('dp') + 1]
    return sk

class AmazonBrowseSpider(JuicerSpider):
    name = 'amazon_browse'
    allowed_domains = ['amazon.com']
    start_urls = gen_start_urls()

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
            hdoc.select('//a[contains(@href, "/b/")]/@href'),
            hdoc.select('//a[contains(@href, "/s/")]/@href'),
            hdoc.select('//a[contains(@href, "/gp/feature.html")]/@href'),
            hdoc.select('//a[contains(@href, "/gp/bestsellers")]/@href'),
            hdoc.select('//a[contains(@href, "/tg/feature")]/@href'),
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(response.url, u) for u in urls]
        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.update_mode = 'custom'
            yield item.process()

        # Terminal urls
        urls = [
            hdoc.select('//a[contains(@href, "/dp/")]/@href'),
            hdoc.select('//a[contains(@href, "/gp/product/")]/@href'),
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(response.url, u) for u in urls]
        for url in urls:
            item = Item(response, HTML)
            item.set('sk', get_sk(url))
            item.set('url', url)
            item.spider = 'amazon_terminal'
            item.update_mode = 'custom'
            yield item.process()

    @staticmethod
    def _update_item(new_data, old_data):
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

SPIDER = AmazonBrowseSpider()
