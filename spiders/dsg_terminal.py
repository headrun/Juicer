from juicer.utils import *
from urlparse import urljoin

def gen_start_urls():
    items = lookup_items('dsg_terminal', 'got_page:False', limit=1000)
    #items = [(None,None,"http://www.dickssportinggoods.com/product/index.jsp?productId=3779427&cp=4406646.4413986.4417717")]
    for _id, term, data in items:
        yield data

class DickssportinggoodsTerminalSpider(JuicerSpider):
    name = 'dsg_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        #sk = response.url
        sk = get_request_url(response).split('productId=')[1]
        sk = sk.split('&cp=')[0]
        price = textify(hdoc.select('//div[@class="op"]/text()')).replace('Price:',' ')
        yousaveprice = textify(hdoc.select('//span[@class="youSave"]/text()')).replace('You save:',' ')
        availability = textify(hdoc.select('//div[@class="availability"]/text()')).replace('Availability:',' ')
        itemnumber = textify(hdoc.select('//span[@class="printBlock"]/text()')).split('Number')[1]
        ref_url = response.url
        item.set('sk',sk)
        item.textify('title', '//h1[@class="productHeading"]')
        item.set('itemnumber', itemnumber)
        item.set('price', price)
        item.set('yousaveprice', yousaveprice)
        item.textify('lpprice', '//span[@class="lp"]')
        item.set('availability', availability)
        item.textify('shippinginfo', '//div[@id="shippingInfo"]//span')
        item.textify('productinfo', '//fieldset[@id="FieldsetProductInfo"]')
        item.textify('image', '//div[@id="galImg"]//a//img/@src')
        item.textify('primarycategory','//div[@id="crumbs"]//a[2]')
        item.textify('secondarycategory','//div[@id="crumbs"]//a[3]')
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

SPIDER = DickssportinggoodsTerminalSpider()

