# This is a template for split crawler terminal. Start using this template by adding your code whereever indicated.
import hashlib

from juicer.utils import *

def gen_start_urls():
    items = lookup_items('insiderpages_terminal', 'got_page:False', limit = 2000 )
    for _id, term, data in items:
        yield data

class InsiderPagesSpider(JuicerSpider):
    name = 'insiderpages_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        # Add Reqd code
        item.set('sk',hashlib.md5(get_request_url(response)).hexdigest())
        item.textify('name','//div[@class="item vcard"]/h1/text()')
        # Address
        key = [textify(k) for k in hdoc.select('//div[@class="item vcard"]//span[@class="adr"]/span/@class') ]
        value = [textify(v) for v in hdoc.select('//div[@class="item vcard"]//span[@class="adr"]/span/text()')]
        item.set('address', dict(zip(key, value)))
        item.textify('desc', '//div[@class="item vcard"]/h5')
        # Telephone
        item.textify('telephone', '//div[@class="item vcard"]//p[@class="tel"]')
        # URL
        item.textify('site_url', '//div[@class="item vcard"]//a[@class="url"]')
        # About
        key = [textify(k) for k in hdoc.select('//dl[@class="info"]//dt')]
        value = [textify(v) for v in hdoc.select('//dl[@class="info"]//dd')]
        item.set('details',dict(zip(key, value)))
        # Reviews
        item.textify('rating','//div[@class="rating_box"]/abbr/@titleC')
        item.textify('review_desc','//div[@class="item vcard"]/h5')
        reviews = hdoc.select('//div[@class="c575 reviewDesc"]')
        reviews = [textify(r) for r in reviews]
        item.set('reviews', reviews)

        item.set('got_page', True)
        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' %got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and 'got_page' not in new_data:
            new_data['got_page'] = old_data['got_page']
        
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data


SPIDER = InsiderPagesSpider()

