from juicer.utils import *

def gen_start_urls():
    items = lookup_items('jigsawcoml_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class JigsawTerminalSpider(JuicerSpider):
    name = 'jigsawcoml_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hxs = HTML(response)
        item = Item(response, HTML)
        overview = textify(hxs.select('//div[@id="wikiSection"]//text()'))
        overview = ' '.join(overview.split())
        industries = textify(hxs.select('//label[contains(text(),"Industries")]//ancestor::td//following-sibling::td//p/text()'))
        industries = ' '.join(industries.split())
        sk = get_request_url(response).split('/')[3]
        #ref_url = response.url
        item.set('sk',sk)
        item.textify('companyname','//p[@id="pageTitle"]')
        item.textify('website','//label[contains(text(),"Website")]//ancestor::td//following-sibling::td//a')
        item.set('overview',overview)
        item.textify('headquarters','//label[contains(text(),"Headquarters")]//ancestor::td//following-sibling::td//p')
        item.textify('phone','//label[contains(text(),"Phone")]//ancestor::td//following-sibling::td')
        item.set('industries',industries)
        item.textify('employees','//label[contains(text(),"Employees")]//ancestor::td//following-sibling::td')
        item.textify('revenue','//label[contains(text(),"Revenue")]//ancestor::td//following-sibling::td')
        item.textify('ownership','//label[contains(text(),"Ownership")]//ancestor::td//following-sibling::td')
        item.set('got_page', True)
        item.set('url', response.url)
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


SPIDER = JigsawTerminalSpider()

