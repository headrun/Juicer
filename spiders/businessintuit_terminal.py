from juicer.utils import *

def gen_start_urls():
    items = lookup_items('businessintuit_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class BusinessintuitTerminalSpider(JuicerSpider):
    name = 'businessintuit_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk',sk)
        item.textify('heading', '//div[@class="portlet"]//h1')
        ratings = textify(hdoc.select('//div[@id="ratingReview"]//a')).replace('\n\t\t\t\t\t reviews', ' ' )
        item.set('ratings', ratings)
        item.textify('phone', '//div[@id="phone"]')
        item.textify('address', '//div[@id="address"]')
        item.textify('img url', '//span[@id="photo"]//img/@src')
        information = {}
        information['keywords'] = textify(hdoc.select('//label[contains(text(),"Keywords")]//following-sibling::span[@class="content"][1]'))
        information['features'] = textify(hdoc.select('//label[contains(text(),"Features")]//following-sibling::span[@class="content"][1]'))
        information['hours'] = textify(hdoc.select('//label[contains(text(),"Hours")]//following-sibling::span[@class="content"]'))
        item.set('information', information)
        item.textify('message', '//div[@id="message"]')
        # Reviews
        nodes = hdoc.select('//div[@class="review"]')
        reviews = {}
        details = []
        for node in nodes:
            name = textify(node.select('.//h3'))
            comment = textify(node.select('.'))
            details.append(name)
            details.append(comment)
            reviews = details
        item.set('reviews', reviews)
        item.set('got_page', True)
        item.update_mode = 'custom'
        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and 'got_page' not in new_data:
            return old_data
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

SPIDER = BusinessintuitTerminalSpider()

