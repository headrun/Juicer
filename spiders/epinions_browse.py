from urlparse import urljoin
from itertools import chain
import hashlib

from juicer.utils import *

def gen_start_urls(name):
    items = get_uncrawled_pages('epinions_browse', limit=100)
    if not items:
        items = [{'url': 'http://www.epinions.com'}]

    for item in items:
        yield item['url']

class EpinionsBrowseSpider(JuicerSpider):
    name = 'epinions_browse'
    allowed_domains = ['epinions.com']
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
            hdoc.select('//table[@id="header"]//td//a/@href'),
            hdoc.select('//dt//h2//a/@href'),
            hdoc.select('//span[@class="rkb"]//a/@href'),
            hdoc.select('//a[contains(text(),"Next")]/@href'),
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(response.url, u) for u in urls]
        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk) 
            item.set('url', url)
            item.set('got_page', False)
            item.update_mode = 'custom'
            yield item.process()

        nodes = hdoc.select('//table//tr[@class="prod"]//td//div//b//a/@href')
        for node in nodes:
            url = textify(node)
            item = Item(response, HTML)
            item.set('sk', url)
            item.set('url', urljoin(response.url, url))
            item.set('got_page', False)
            item.spider = 'epinions_terminal'
            item.update_mode = 'custom'
            yield item.process()

SPIDER = EpinionsBrowseSpider()
