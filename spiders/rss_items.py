from juicer.utils import *
from itertools import chain
from urlparse import urljoin
import hashlib
#When HR and proxy is on the framework uncomment the line below
from cloudlibs import proxy

hash_url = lambda url: hashlib.md5(url).hexdigest()

SERVICE_ADDRESS = 'http://framework.h.com/text_extractor/'

class RssItemsSpider(JuicerSpider):
    name = 'rss_items'
    #start_urls gets the urls from gen_start_urls function

    def start_requests(self):
        requests = []
        items = lookup_items('rss_items', 'got_page:False', limit=1000)
        for _id, term, data in items:
            data = eval(data)
            requests.extend(Request(data['link'], self.parse, None, meta=data))


        return requests


    def parse(self, response):
        body = response.body

        meta = response.meta
        sk = meta['sk']

        #send body to Text-Extractor Service
        p = proxy(SERVICE_ADDRESS)

        #removing bad data from body
        body = body.decode('utf8','ignore')
        result = p.process_text(body)

        text = ''
        if result.has_key('data'):
            result = result['data']
        text = result.get('text', '')

        item = Item(response, HTML)
        item.set('sk', sk)
        item.set('text', text)
        item.set('extracted', True)
        item.set('got_page', True)
        item.update_mode = 'custom'

        yield item.process()

    @staticmethod
    def _update_item(new_data, old_data):
        #this function updates an item's existing data with new data
        # in this case, only if got_page is false it will update
        # if true, i do not want to change it to false otherwise it will crawl again later on.

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
        link = item['link']

        if not link:
            return []
        got_page = item.get('got_page', False)

        tokenized = item.get('tokenized', False)
        data = {'link':link, 'sk':item['sk']}

        text = item.get('text', '')
        updated = item.get('updated')
        #TODO change to date created instead of date updated
        to_be_tokenized_data = {'text':text, 'updated':updated, 'sk':item['sk']}

        extracted = item.get('extracted', False)
        return [('got_page:%s' % got_page, repr(data)), ('text_extracted:%s;is_tokenized:%s' % (extracted, tokenized), repr(to_be_tokenized_data))]

SPIDER = RssItemsSpider()
