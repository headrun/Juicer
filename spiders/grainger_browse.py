# This was written by Jatin Verma on 17.08.2011

from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls(name):
    items = lookup_items('grainger_browse', 'got_page:False', limit = 2000)
    if not items:
        items = [(None, None, 'http://www.grainger.com/sitemap')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

class GraingerBrowseSpider(JuicerSpider):
    name = 'grainger_browse'
    allowed_domains = ['http://www.grainger.com']
    start_urls =  gen_start_urls(name)

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk = hashlib.md5(response.url).hexdigest()
        item.set('sk', sk)
        item.set('got_page', True)
        item.set('url', response.url)
        item.update_mode = 'custom'
        yield item.process()

        urls = [
            # Add hdoc.select('Xpath') Here
            hdoc.select('//div[@id="static"]/div[@class="colI"]//li/a/@href'),
            hdoc.select('//div[@class="searchNavPaneTitlePane"][1]//li/a/@href'),
            hdoc.select('//span[@class="paginationContainer"]//li/a[contains(text(),"Next")]/@href')
        ]

        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [u if 'www.grainer.com' in u else urljoin(get_request_url(response), u) for u in urls]

        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.update_mode = 'custom'
            item.set('got_page', False)
            yield item.process()


        # Terminal Urls
        urls = [
            hdoc.select('//div[@class="itemLink"]/a/@href')
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(response.url, u) for u in urls]
        for url in urls:
            item = Item(response, HTML)
            # item.set('sk', get_sk(url))
            item.set('url', url)
            sk = url.split('-')[-1]
            item.set('sk', sk)
            item.spider = 'grainger_terminal'
            item.update_mode = 'custom'
            item.set('got_page', False)
            yield item.process()


    @staticmethod
    def _update_item(new_data, old_data):
        #this function updates an item's existing data with new data
        #in this case, only if got_page is false it will update
        #if true, i do not want to change it to false otherwise it will crawl again later on.
        if 'got_page' in old_data and 'got_page' not in new_data:
            new_data['got_page'] = old_data['got_page']

        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

    @staticmethod
    def _index_item(item):
        #when consumedata takes place, since _index_item exists, this function is executed
        #the values returned here are stored in a table called data_index
        #the first element in the tuple is "term" whose value is the gotpage value
        #the second element in tuple is "data" which is the url
        #so when gen_start_urls is called by a spider, query is happening by term, choosing those
        #terms whose got_page is false, and we take only the data part which is the url

        got_page = item.get('got_page', False)
        return [('got_page:%s' %got_page, item['url'])]

SPIDER = GraingerBrowseSpider()

