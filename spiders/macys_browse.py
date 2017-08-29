from urlparse import urljoin
import hashlib
import re

from juicer.utils import *

def gen_start_urls(name):
    items = lookup_items('macys_browse', 'got_page:False', limit=1000)
    if not items:
        items = [(None, None, 'http://www1.macys.com/index.ognc')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

class MacysSpider(JuicerSpider):
    name = 'macys_browse'
    allowed_domains = ['macys.com']
    start_urls = gen_start_urls(name)

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        url  = get_request_url(response)
        sk = hashlib.md5(url).hexdigest()
        item.set('sk', sk)
        item.set('got_page', True)
        item.set('url', url)
        item.update_mode = 'custom'
        yield item.process()

        urls = [
            hdoc.select('//ul[@class="globalNavigationBar"]//li//a/@href'),
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(url, u) for u in urls]

        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.set('got_page', False)
            item.update_mode = 'custom'
            yield item.process()

        for url in hdoc.select('//ul[@class="nav_cat_sub_3"]//li//a/@href'):
            url = textify(url)
            cat_id = re.findall('=(.*?)&', url) or re.findall('=(.*)', url)

            if not cat_id:
                continue

            url = urljoin(response.url, '/catalog/category/facetedmeta?edge=hybrid&categoryId=%s&pageIndex=1&sortBy=ORIGINAL&productsPerPage=100&&intl=true' % cat_id[0])
            yield Request(url, self.parse_details, response, meta={'cat_id': cat_id[0]})

        for node in hdoc.select('//a[@class="imageLink productThumbnailLink absolutecrossfade"]/@href'):
            node = textify(node)
            item = Item(response, HTML)
            item.set('sk', node.split('ID=')[1].split('&')[0])
            item.set('url', node)
            item.set('got_page', False)
            item.spider = 'macys_terminal'
            item.update_mode = 'custom'
            yield item.process()

    def parse_details(self, response):
        hdoc = HTML(response)

        cat_id = response.meta.get('cat_id')
        prod_ids = eval(textify(hdoc.select('//p')))['productIds']
        prod_ids = ','.join([cat_id + '_' + str(p_id) for p_id in prod_ids])

        url = urljoin(response.url, '/shop/catalog/product/thumbnail/1?edge=hybrid&limit=none&categoryId=%s&ids=%s' % (cat_id, prod_ids))
        sk = hashlib.md5(url).hexdigest()
        item = Item(response, HTML)
        item.set('sk', sk)
        item.set('url', url)
        item.set('got_page', False)
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

SPIDER = MacysSpider()
