from itertools import chain
from juicer.utils import *

class Spider(JuicerSpider):
    name = 'generic_terminal'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        hdoc = HTML(response)

    @staticmethod
    def _update_item(new_data, old_data):
        old_from_urls = old_data.get('from_urls', [])
        new_from_urls = new_data.get('from_urls', [])
        all_from_urls = list(chain(old_from_urls, new_from_urls))

        data = {}
        data.update(old_data)
        data.update(new_data)
        data['from_urls'] = all_from_urls

        return data

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('%s:got_page:%s' % (item['url'], got_page), item['url'])]

SPIDER = Spider()
