from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls():
    items = lookup_items('99acres_browse', 'got_page:False', limit=100)
    if not items:
        items = [(None, None, 'http://www.99acres.com')]
    for _id, term, data in items:
        yield data


class AcresSpider(JuicerSpider):
    name = '99acres_browse'
    allowed_domains = ['99acres.com']
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
            hdoc.select('//div[@id="rescom"]//span//a/@href'),
            hdoc.select('//div[@class="cities f11"]/a/@href'),
            hdoc.select('//a[contains(text(), "Next")]/@href'),
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

        terminals = hdoc.select('//a[@class="f13 b"]/@href')
        for terminal_url in terminals:
            terminal_url = textify(terminal_url)
            sk = terminal_url.split('-')[-1]
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url',"http://www.99acres.com"+terminal_url)
            item.set('got_page', False)
            item.spider = '99acres_terminal'
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

SPIDER = AcresSpider()

