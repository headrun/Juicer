from juicer.utils import *
from urlparse import urljoin

def gen_start_urls():
    items = lookup_items('borders_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class BordersTerminalSpider(JuicerSpider):
    name = 'borders_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        # sk = response.url
        sk = get_request_url(response).split('?sku=')[1]
        publisher = textify(hdoc.select('//b[contains(text(),"Publisher")]//parent::div/text()'))
        date = textify(hdoc.select('//b[contains(text(),"Date")]//parent::div/text()')).replace('Date',' ')
        edition  = textify(hdoc.select('//b[contains(text(),"Edition")]//parent::div/text()')).replace('Edition',' ')
        isbn13 = textify(hdoc.select('//b[contains(text(),"ISBN13")]//parent::div/text()')).replace('ISBN13',' ')
        isbn = textify(hdoc.select('//b[contains(text(),"ISBN:")]//parent::div/text()')).replace('ISBN:',' ')
        binc = textify(hdoc.select('//b[contains(text(),"BINC:")]//parent::div/text()')).replace('BINC:',' ')
        age = textify(hdoc.select('//b[contains(text(),"Age:")]//parent::div/text()')).replace('Age:',' ')
        ref_url = response.url
        item.set('sk', sk)
        item.textify('title', '//h1[@class="titleheader"]')
        item.textify('image', '//img[@class="jtip prod-item"]/@src')
        item.textify('description', ('//p[@class="about-product-ctw"]', '//p[@class="about-product-ctw"]//following-sibling::p/text()'))
       # item.textify('description', ('//p[@class="about-product-ctw"]', '//p[@class="about-product-ctw"]//following-sibling::div[1]'))
        item.textify('offerprice', '//div[@class="offerPrice_enhancedTDP"]//b')
        item.textify('listprice', '//div[@class="enhanced_listprice"]')
        item.textify('yousave', '//div[@class="enhanced_saleprice"]')
        item.set('publisher', publisher)
        item.set('date', date)
        item.set('edition', edition)
        item.set('isbn13', isbn13)
        item.set('isbn', isbn)
        item.set('binc', binc)
        item.set('age', age)
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


SPIDER = BordersTerminalSpider()

