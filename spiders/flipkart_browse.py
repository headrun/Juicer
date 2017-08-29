#modified amazon_browse.py to suit flipkart_browse.py

from juicer.utils import *
from itertools import chain
from urlparse import urljoin
import hashlib

def gen_start_urls(name):
    items = lookup_items('flipkart_browse', 'got_page:False', limit=2000)
    for _id, term, data in items:
        yield data

def get_sk(url,hdoc):
    sk = None
    if hdoc.select("//div[@class='fk-mprod-shipping-section-id']"):#Terminal Page
        sk = url.rsplit('?')[0]
    else: #Browse Page / Non-Terminal Page
        sk = hashlib.md5(url).hexdigest()

    return sk

class FlipkartBrowseSpider(JuicerSpider):
    name = 'flipkart_browse'
    allowed_domains = ['flipkart.com']
    start_urls = gen_start_urls(name)

    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)
        item.set('sk', get_sk(get_request_url(response), hdoc))
        item.set('got_page', True)
        item.set('url', get_request_url(response))
        item.update_mode = 'custom'
        yield item.process()

        urls = hdoc.select('//a/@href')

        urls = [textify(u) for u in urls]
        urls = [urljoin(get_request_url(response), u) for u in urls]

        restricted_urls = ['/s/help/payments/cod',
                           '/account/?rd=0',
                           '/wishlist',
                           '/s/contact',
                           '/account/login',
                           '/account/',
                           '/s/help/payments',
                           '/s/help/shipping',
                           '/s/help/cancellation-returns',
                           '/s/help',
                           '/s/contact',
                           '/s/about',
                           '/s/careers',
                           '/s/press',
                           '/affiliate/',
                           '/buy-gift-voucher',
                           '/s/terms',
                           '/s/paymentsecurity',
                           '/s/privacypolicy']

        restricted_urls = [urljoin(get_request_url(response), u) for u in restricted_urls]

        for url in urls:
            if url in restricted_urls:
                continue

            item = Item(response, HTML)
            item.set('sk', get_sk(url,hdoc))
            item.set('url', url)
            item.update_mode = 'custom'

            if hdoc.select("//div[@class='fk-mprod-shipping-section-id']"):#Terminal Page
                item.spider = 'flipkart_terminal'

            item.set('got_page',False)
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

SPIDER = FlipkartBrowseSpider()

