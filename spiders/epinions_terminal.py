from urlparse import urljoin

from juicer.utils import *

def gen_start_urls():
    items = lookup_items('epinions_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class EpinionsTerminalSpider(JuicerSpider):
    name = 'epinions_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = response.url
        ref_url = response.url
        item.set('sk',sk)
        item.textify('title', '//h1[@class="title"]')
        item.textify('overallrating', ('//table//tr//td//div//span[@class="rkr"]', '//span[@class="rkb"]//img/@alt'))
        item.textify('image', '//img[@name="product_image"]/@src')
        item.textify('mpn', '//td[contains(text(),"MPN:")]//following-sibling::td')
        item.textify('usercontrols', '//td[contains(text(),"User Controls")]//following-sibling::td')
        item.textify('upc', '//td[contains(text(),"UPC")]//following-sibling::td')
        item.textify('productid', '//td[contains(text(),"Product ID")]//following-sibling::td')
        item.textify('resolutionssupported', '//td[contains(text(),"Resolutions supported")]//following-sibling::td')
        item.textify('nativeresolution', '//td[contains(text(),"Native (Recommended) Resolution")]//following-sibling::td')
        item.textify('vewdtails', '//table[@id="product_spec"]')
        item.textify('details', '//td[contains(text(),"Details")]//following-sibling::td')
        item.textify('lowestprice', '//span[contains(text(),"Lowest Price:")]//child::span')
        item.set('got_page', True)
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


SPIDER = EpinionsTerminalSpider()

