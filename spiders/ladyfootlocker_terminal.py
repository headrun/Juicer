from juicer.utils import *
from urlparse import urljoin

def gen_start_urls():
    items = lookup_items('ladyfootlocker_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class LadyfootlockerTerminalSpider(JuicerSpider):
    name = 'ladyfootlocker_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('model--')[1]
        sk = sk.split('/')[0]
      #  ref_url = response.url
        item.set('sk',sk)
        item.textify('title', '//div[@id="pdp_info"]//h1')
        item.textify('price', '//p[@id="pdp_priceRange"]')
        item.textify('selectedstyle', '//span[@id="productAttributes"]')
        item.textify('size', '//div[@id="pdp_sizeAvailableWrapper"]//following-sibling::ul//li//a')
        item.textify('productsku', '//span[@id="productSKU"]')
        item.textify('description', '//table[@class="product_description"]')
        item.textify('image', '//a[@id="productImage"]//img/@src')
        item.textify('primarycategory', '//div[@class="breadCrumb"]')
        item.set('url', response.url)
        item.update_mode = 'custom'
        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and 'got_page' not in new_data:
            new_data['got_page'] = old_data['got_page']

        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

SPIDER = LadyfootlockerTerminalSpider()

