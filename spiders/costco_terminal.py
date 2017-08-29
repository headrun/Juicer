from juicer.utils import *
from urlparse import urljoin

def gen_start_urls():
    items = lookup_items('costco_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class CostcoTerminalSpider(JuicerSpider):
    name = 'costco_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        sk = get_request_url(response).split('?Prodid=')[1]
        sk = sk.split('&Ne=')[0]
        #ref_url = response.url
        image = textify(hdoc.select('//img[@name="ProductImage"]/@src'))
        item.set('sk', sk)
        item.textify('title', '//span[@id="ProductMainInfo_ProductTitle"]')
        item.textify('description', '//div[@id="ProductInfoTabs_ProductDetailsTab"]')
        item.textify('price', '//span[@id="ProductMainInfo_Price"]')
        item.textify('merchandisingdesc', '//span[@id="ProductMainInfo_MerchandisingDesc"]')
        item.textify('itemnumber', '//span[@id="ProductMainInfo_ItemNumber"]')
        item.textify('partnumber', '//span[@class="Model"]')
        item.set('image', "http:" + image)
        item.textify('primarycategory', '//a[@name="CategoryLink1"][1]')
        item.textify('secondarycategory', '//a[@name="CategoryLink1"][2]')
        item.textify('tertiarycategory', '//a[@name="CategoryLink1"][3]')
        item.textify('shippingterms', '//div[@id="ProductInfoTabs_ShippingInfoTab"]')
        item.textify('productreview', '//div[@id="NoReviewsYet"]')
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

SPIDER = CostcoTerminalSpider()
