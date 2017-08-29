from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls(name):
    items = lookup_items('businessintuit_browse', 'got_page:False', limit=10)
    if not items:
        items = [(None, None, 'http://business.intuit.com/directory/')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

class BusinessintuitSpider(JuicerSpider):
    name = 'businessintuit_browse'
    allowed_domains = ['business.intuit.com']
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
            [textify(u) + '?showAllCities=1' for u in hdoc.select('//h3[contains(text(),"Browse cities by state")]//following-sibling::ul[1]//li//a/@href')],
            # hdoc.select('//div[@class="moreLink"]//a/@href'),
            hdoc.select('//div[@id="stateCities"]//span//a/@href'),
            hdoc.select('//span[@class="link"]//a[@class="title"]/@href'),
            hdoc.select('//div[@class="searchFooterPad"]//a[contains(text(),"next")]/@href')
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

        terminals = hdoc.select('//div[@class="data"]//h2//a/@href')
        for terminal_url in terminals:
            terminal_url = urljoin('http://business.intuit.com/', textify(terminal_url))
            item = Item(response, HTML)
            item.set('sk', terminal_url)
            item.set('url', terminal_url)
            item.set('got_page', False)
            item.spider = 'businessintuit_terminal'
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

SPIDER = BusinessintuitSpider()

