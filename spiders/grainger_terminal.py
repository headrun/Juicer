# Written by Jatin Verma on 17.08.2011.

from juicer.utils import *

def gen_start_urls():
    items = lookup_items('grainger_terminal', 'got_page:False', limit = 2000 )
    print "in gen)start_urls"
    for _id, term, data in items:
        print data
        yield data

class GraingerTerminalSpider(JuicerSpider):
    name = 'grainger_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        item.set('sk', get_request_url(response).split('-')[-1])
        
        container = hdoc.select('//div[@id="DetailTable"]')
        keys = container.select('.//tr/td[1]')
        keys = [textify(k) for k in keys]
        values = container.select('.//tr/td[2]')
        values = [textify(v) for v in values]
        details = dict(zip(keys, values))

        container2 = hdoc.select('//div[@id="TechSpecColumn"]')
        keys = container2.select('.//tr/td[1]')
        keys = [textify(k) for k in keys]
        values = container2.select('.//tr/td[3]')
        values = [textify(v) for v in values]
        tech_specs = dict(zip(keys, values))
        #print details, tech_specs
        # Add Reqd code
        item.textify('image', '//div[@id="ItemImage"]/img/@src')
        item.set('details', details)
        item.set('tech_specs', tech_specs)
        item.set('got_page', True)
        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' %got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and 'got_page' not in new_data:
            new_data['got_page'] = old_data['got_page']

        data = {}
        data.update(old_data)
        data.update(new_data)
        return data


SPIDER = GraingerTerminalSpider()

