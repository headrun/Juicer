from juicer.utils import *
from urlparse import urljoin

def gen_start_urls():
    items = lookup_items('macys_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class MacysTerminalSpider(JuicerSpider):
    name = 'macys_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('ID=')[1]
        sk = sk.split('&')[0]
        name = textify(hdoc.select('//h1[@class="productDetailShort"]'))
        item.textify('name', '//div[@class="depthpathContainer"]')
        item.textify('detailprice','//div[@id="bag_buttons"]//div[@class="standard_prod_pricing_group"]//span[@class="productDetailPrice"]')
        item.textify('detailsale','//div[@id="bag_buttons"]//div[@class="standard_prod_pricing_group"]//span[@class="productDetailSale"]')
        item.textify('keywords', '//div[@class="depthpathContainer"]')
        item.textify('description','//div[@id="productDetailSection"]//div[@class="productDetailLong"]')
        item.textify('details','//div[@id="pdpInfoTab1_content"]//ul//li')
        item.textify('image','//noscript//img/@src')
        item.textify('primarycategory','//div[@class="breadCrumbs"]//h2[1]//a')
        item.textify('secondarycategory','//div[@class="breadCrumbs"]//h2[2]//a')
        item.textify('tertiarycategory','//h1[@class="depthPathActive"]')
        item.textify('size','//option[contains(text(),"Select Size")]//following-sibling::option')
        item.textify('color','//option[contains(text(),"Select Color")]//following-sibling::option')
        item.set('sk', sk)
        item.set('got_page', True)
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


SPIDER = MacysTerminalSpider()

