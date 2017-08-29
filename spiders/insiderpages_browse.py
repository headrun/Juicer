# This is a template for split crawler- browse.
# Just copy this template to the appropriate name and start writing your crawler specific code

from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls(name):
    items = lookup_items('insiderpages_browse','got_page:False',limit = 20000)
    if not items:
        items = [(None, None, 'http://www.insiderpages.com/states')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

class InsiderPagesSpider(JuicerSpider):
    name = 'insiderpages_browse'
    allowed_domains = ['http://www.insiderpages.com']
    start_urls =  gen_start_urls(name)

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        urls = [
            hdoc.select('//table[@class="city_navigation"][2]//td/a/@href'),
            ['/browse' + textify(city) for city in hdoc.select('//div[@class="city_letter"]/following-sibling::p[1]//a/@href')],
            hdoc.select('//div[@class="search_biz"]/strong/a/@href'),
            hdoc.select('//div[@class="content_column"]/a/@href'),
        ]

        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        # import pdb; pdb.set_trace()
        urls = [urljoin(get_request_url(response) , u) for u in urls]
        
        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.set('got_page', False)
            item.update_mode = 'custom'
            yield item.process()

        # Listing Page
        nodes = [ textify(u) for u in hdoc.select('//div[@id="search_results"]//h2/a/@href') ]
        for terminal_url in nodes:
            terminal_url = urljoin('http://www.insiderpages.com',terminal_url)

            item = Item(response, HTML)
            item.set('sk', terminal_url)
            item.set('url', terminal_url)
            item.set('got_page', False)
            item.spider = 'insiderpages_terminal'
            item.update_mode = 'custom'
            
            yield item.process()

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and 'got_page' not in new_data:
            new_data['got_page'] = old_data['got_page']

        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

    @staticmethod
    def _index_item(item):

        got_page = item.get('got_page', False)
        return [('got_page:%s' %got_page, item['url'])]

SPIDER = InsiderPagesSpider()
 
