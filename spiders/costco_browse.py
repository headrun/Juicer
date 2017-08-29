from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls(name):
    items = lookup_items('costco_browse', 'got_page:False', limit=100)
    if not items:
        items = [(None, None, 'http://www.costco.com/Browse/MainShop.aspx?cat=24091&eCat=BC|24091&lang=en-US&whse=BC&topnav=')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data


class CostcoBrowseSpider(JuicerSpider):
    name = 'costco_browse'
    allowed_domains = ['costco.com']
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
            hdoc.select('//table[@id="CatTable"]//a[@class="catlink"]/@href'),
            hdoc.select('//div[@class="t11 darkgray2 bgGray2 p2"]//li[@class="leftNavMainSubCategory leftNavMainSubCategoryNoArrow"]//a/@href'),
            hdoc.select('//img[@title="next page"]//parent::a/@href')
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

        nodes = hdoc.select('//td[@class="t11 darkblue2 b"]//a/@href')
        for node in nodes:
            url = textify(node)
            item = Item(response, HTML)
            item.set('sk', url)
            item.set('url', urljoin(response.url, url))
            item.set('got_page', False)
            item.spider = 'costco_terminal'
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

SPIDER = CostcoBrowseSpider()
