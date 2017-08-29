from juicer.utils import *
def gen_start_urls():
    items = lookup_items('yellowbook_terminal', 'got_page:False', limit=10)
    for _id, term, data in items:
        yield data

class YellowbookTerminalSpider(JuicerSpider):
    name = 'yellowbook_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('_')[-1]
        sk = sk.split('.html?')[0]
        item.set('sk',sk)
        item.textify('heading', '//div[@class="vcard"]//h1')
        item.textify('address', '//span[@class="street-address"]')
        item.textify('locality', '//span[@class="locality"]')
        item.textify('region', '//span[@class="region"]')
        item.textify('postal code', '//span[@class="postal-code"]')
        item.textify('phone', '//span[@class="value"]')
        item.textify('visit', '//div[@class="url"]')
        item.textify('num. of reviews', '//div[@class="profileReviewAvg"]')
        item.textify('information', '//div[@class="profileContentBlock"]//dl//dd')
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
            return old_data
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data


SPIDER = YellowbookTerminalSpider()


