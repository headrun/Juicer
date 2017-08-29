from urlparse import urljoin

from juicer.utils import *

def gen_start_urls():
    items = lookup_items('stevemadden_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class StevemaddenTerminalSpider(JuicerSpider):
    name = 'stevemadden_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        #sk = response.url
        sk = get_request_url(response).split('id=')[1]
        image = textify(hdoc.select('//a[@class="thumb-view view-Nav selected"]//img[@class="view-image-thumb-nonflash"]/@src'))
        ref_url = response.url
        item.set('sk',sk)
        item.textify('title', '//h1')
        item.textify('item-original-price', '//div[@class="item-price-wrapper"]//span[@class="item-original-price"]')
        item.textify('item-price', '//div[@class="item-price-wrapper"]//span[@class="item-price"]')
        item.textify('description', '//div[@id="description"]')
        item.set('image', "http:"+image)
        item.set('got_page', True)
        item.set('url', get_request_url(response))
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

SPIDER = StevemaddenTerminalSpider()

