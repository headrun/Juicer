from juicer.utils import *

class EtsyTerminalSpider(JuicerSpider):
    name = 'etsy_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/listing/')[-1]
        sk = sk.split('/')[0]
        item.set('sk', sk)
        item.textify('title', '//div[@id="item-title"]//h1')
        item.textify('large_img', '//div[@id="fullimage_link1"]//img/@src')
        item.textify('small_img', '//div[@id="item-thumbs"]//img//@src')
        item.textify('description', '//div[@class="section-content"]')
        properties = textify(hdoc.select('//h3[contains(text(),"About this item")]//following-sibling::p')).replace('\n', '').replace('\t', '')
        item.set('properties', properties)
        item.textify('tags', '//div[@id="item-tags"]//div//a')
        item.textify('materials', '//div[@id="item-materials"]//div//a')
        price = textify(hdoc.select('//div[@class="item-amount"]/text()')).split(' ')[0]
        item.set('price', price)
        availability = textify(hdoc.select('//div[@class="item-stock"]')).split('\n')[0]
        item.set('availability', availability)
        yield item.process()
        got_page(self.name, response)
