from juicer.utils import *
from urlparse import urljoin

def gen_start_urls():
    items = lookup_items('beautylish_terminal', 'got_page:False', limit=1000)
    #items = [(None,None,"http://www.beautylish.com/p/loreal-carbon-black-volume-building-mascara")]
    for _id, term, data in items:
        yield data

class BeautylishTerminalSpider(JuicerSpider):
    name = 'beautylish_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk',sk)
        item.textify('title', '//h1[@class="h1"]')
        item.textify('image', '//img[@id="product-image"]/@src')
        item.textify('menu_name', '//h1[@class="h1"]//a')
        item.textify('products', '//a[@class="inlineblock meta meta_title neutral neutral_link"]')
        item.textify('description', '//div[@class="mod vmod"]//div[@class="inner "]//p')
        item.textify('productavailability', '//a[@class="link"]')
        data = []
        nodes = hdoc.select('//div[@class="body media mb0"]')
        for node in nodes:
            details = {}
            details['username'] = textify(node.select('.//a[@class="fn fwb url"]'))
            details['userimage'] = textify(node.select('.//span[@class="img"]//a//img/@src'))
            details['reviewtitle'] = textify(node.select('.//div[@class="meta meta_title neutral"]'))
            details['reviewdate'] = textify(node.select('.//li[@class="meta neutral"]'))
            details['reviewdescription'] = textify(node.select('.//p'))
            data.append(details)
            #print '1',data
        revw_next = hdoc.select('//a[contains(text(),"next")]/@href')
        yield Request(revw_next, self.parse_reviews, response, meta={'data':data, 'item':item})

    def parse_reviews(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        data = response.meta.get('data')
        item = response.meta.get('item')
        nodes = hdoc.select('//div[@class="body media mb0"]')
        for node in nodes:
            details = {}
            details['username'] = textify(node.select('.//a[@class="fn fwb url"]'))
            details['reviewtitle'] = textify(node.select('.//div[@class="meta meta_title neutral"]'))
            details['userimage'] = textify(node.select('.//span[@class="img"]//a//img/@src'))
            details['reviewdate'] = textify(node.select('.//li[@class="meta neutral"]'))
            details['reviewdescription'] = textify(node.select('.//p'))
            data.append(details)
        revw_next = hdoc.select('//a[contains(text(),"next")]/@href')
        if revw_next:
            yield Request(revw_next, self.parse_reviews, response, meta={'data':data, 'item':item})
        else:
            item.set('data', data)
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

SPIDER = BeautylishTerminalSpider()

