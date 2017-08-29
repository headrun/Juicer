from juicer.utils import *
from urlparse import urljoin
import hashlib

def gen_start_urls(name):
    items = lookup_items('jcpenney_browse', 'got_page:False', limit=100)
    if not items:
        items = [(None, None, 'http://www.jcpenney.com/jcp/default.aspx')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

class JcpenneyBrowseSpider(JuicerSpider):
    name = 'jcpenney_browse'
    allowed_domains = ['jcpenney.com']
    start_urls = gen_start_urls(name)

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
            hdoc.select('//ul[@id="nm_tabs"]//li//a/@href'),
            hdoc.select('//ul[@class="sideNav"]//li//a/@href'),
            hdoc.select('//img[@title="Go to next page"]//ancestor::a/@href')
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        for url in urls:
            if 'http://www.jcpenney.com/jcp/' not in url:
                url = 'http://www.jcpenney.com/jcp/' + url
            else:
             sk = hashlib.md5(url).hexdigest()
             item = Item(response, HTML)
             item.set('sk', sk)
             item.set('url', url)
             item.set('got_page', False)
             item.update_mode = 'custom'
             yield item.process()

        nodes = hdoc.select('//div[@class="ThumbTab"]//a/@href')
        for node in nodes:
            url = textify(node)
            item = Item(response, HTML)
            item.set('sk', url.split('&')[1])
            item.set('url', urljoin(response.url, url))
            item.set('got_page', False)
            item.spider = 'jcpenney_terminal'
            item.update_mode = 'custom'
            yield item.process()
    
    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and old_data['got_page'] == True:
            return old_data

        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

SPIDER = JcpenneyBrowseSpider()

