from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls(name):
    items = lookup_items('yellowbook_browse', 'got_page:False', limit=10)
    if not items:
        items = [(None, None, 'http://www.yellowbook.com/change-location/?originpage=homepage')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

class YellowbookSpider(JuicerSpider):
    name = 'yellowbook_browse'
    allowed_domains = ['yellowbook.com']
    start_urls = gen_start_urls(name)

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = hashlib.md5(get_request_url(response)).hexdigest()
        item.set('sk', sk)
        item.set('got_page', True)
        item.set('url', response.url)
        item.update_mode = 'custom'
        yield item.process()

        urls = [
            hdoc.select('//div[@class="contentBiz"]//ul//li//a/@href'),
            hdoc.select('//div[@id="homeLeft-cont"]//h1//a/@href'),
            hdoc.select('//div[@class="category-wrap"]//ul[@class="clear-wrap"]//li//a/@href'),
            hdoc.select('//li[@class="pagControl "]//a/@href[1]')
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(get_request_url(response), u) for u in urls]
        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.set('got_page', False)
            item.update_mode = 'custom'
            yield item.process()

        terminals = hdoc.select('//div[@class="bizName clearBlock"]//h2//a/@href')
        for terminal_url in terminals:
            terminal_url = urljoin('http://www.yellowbook.com/', textify(terminal_url))
            item = Item(response, HTML)
            item.set('sk', terminal_url.split('_')[-1].split('.html?')[0])
            item.set('url', terminal_url)
            item.set('got_page', False)
            item.spider = 'yellowbook_terminal'
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

SPIDER = YellowbookSpider()
