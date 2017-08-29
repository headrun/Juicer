from juicer.utils import *
from urlparse import urljoin
import hashlib

def gen_start_urls(name):
    items = lookup_items('jigsawcoml_browse', 'got_page:False', limit=1000)
    if not items:
        items = [(None, None, 'http://www.jigsaw.com/geography/us/company-information-list.xhtml')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

class JigsawBrowseSpider(JuicerSpider):
    name = 'jigsawcoml_browse'
    allowed_domains = ['jigsaw.com']
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
            hdoc.select('//tbody//tr//td//a/@href'),
            hdoc.select('//td[@class="tblrowLeft"]//a/@href'),
        ]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        urls = [urljoin(('/'.join((response.url).split('/')[:-1])), u) for u in urls]
        for url in urls:
            sk = hashlib.md5(url).hexdigest()
            item = Item(response, HTML)
            item.set('sk', sk)
            item.set('url', url)
            item.update_mode = 'custom'
            yield item.process()

        total_recs = textify(hdoc.select('//input[@name="recordCount"]/@value'))
        if total_recs:
            total = int(total_recs)/200
            ref_url = response.url
            k = ref_url.split('/')
            page_count = 2 
            for record in range(total):
                page_count = int(page_count) + 1
                k[3] = str(page_count)
                next_page_url = '/'.join(k)
               #sk = hashlib.md5().hexdigest()
                item = Item(response, HTML)
                item.set('sk', next_page_url)
                item.set('url', next_page_url)
                item.set('got_page', False)
                item.update_mode = 'custom'
                yield item.process()

        nodes = hdoc.select('//td[@class="tblrowLeft"]//a/@href')
        for node in nodes:
                url = textify(node)
                item = Item(response, HTML)
                item.set('sk', url.split('/')[1])
                item.set('url', urljoin(response.url, url))
                item.set('got_page', False)
                item.spider = 'jigsawcoml_terminal'
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

SPIDER = JigsawBrowseSpider()

