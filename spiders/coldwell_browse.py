import re
import hashlib
from urlparse import urljoin
from datetime import datetime

from juicer.utils import *

#NOTE: Recent listings requires login , needs to bo integrated

def gen_start_urls():
    items = lookup_items('coldwell_browse', 'got_page:False', limit=100)
    if not items:
        items = [(None, None, 'http://www.coldwellbanker.com/real_estate/home_search')]
    for _id, term, data in items:
        yield remove_sid(data)

def get_sk(url):
    pid = re.findall("propertyId=(.*?)&", url)
    pid = pid[0]
    return pid

def remove_sid(url):
    u = re.findall("(\;jsessionid.*?node[0-9]{2})", url)
    if u:
        url = url.replace(u[0], '')
    return url

class ColdWellBankerSpider(JuicerSpider):
    name = 'coldwell_browse'
    allowed_domains = ['coldwellbanker.com']
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        url = remove_sid(response.url)
        sk = hashlib.md5(response.url).hexdigest()
        item.set('sk', sk)
        item.set('got_page', True)
        item.set('url', url)
        item.update_mode = 'custom'
        yield item.process()

        urls = [

            #state links

            hdoc.select('//ul[@class = "usStatesColumn"]//a[contains(@href, "real_estate/home_search/")]/@href'),
            hdoc.select('//ul[@class = "canadaColumn"]//a[contains(@href, "/property")]/@href'),

            #get usa city links
            hdoc.select('//a[contains(@href, "../../real_estate/home_search/")]/@href'),

            # get usa city listing page links
            hdoc.select('//ul[@class = "propertyListing"]/following-sibling::a/@href'),

            #next page link
            hdoc.select('//a[@class = "btn_next"]/@href')

        ]

        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(response.url, u) for u in urls]
        urls = [remove_sid(url) for url in urls]

        for url in urls:
            sk = hashlib.md5(url).hexdigest()

            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.set('got_page', False)
            item.update_mode = 'custom'
            yield item.process()

        #terminal urls

        urls = [
            hdoc.select('//div[@class = "propertyViewLink"]/a/@href')
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(response.url, u) for u in urls]
        urls = [remove_sid(url) for url in urls]

        for url in urls:
            item = Item(response, HTML)
            item.set('sk', get_sk(url))
            item.set('url', url)
            item.set('got_page', False)
            item.spider = 'coldwell_terminal'
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


SPIDER = ColdWellBankerSpider()
