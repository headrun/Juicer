from juicer.utils import *

class MyntraTerminalSpider(JuicerSpider):
    name = 'myntra_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-2]
        sizes = hdoc.select('//div[@id="size-options"]//a')
        sizes = [textify(s) for s in sizes]
        item.set('sizes', sizes)
        item.textify('title', '//div[@class="title-strip"]//h1')
        item.textify('actual_price', '//span[@class="mrp"]//b')
        item.textify('description', '//div[@class="product-description black-bg5 corners-bl-br"]//p')
        item.textify('specifications','//div[@class="product-description black-bg5 corners-bl-br"]//ul//li')
        item.textify('savings from site', '//div[@class="nav-buttons"]//div[@class="discount-label val"]//span')
        item.textify('price', '//span[@class="dis-price"]//strong')
        yield item.set_many({'sk': sk}).process()
