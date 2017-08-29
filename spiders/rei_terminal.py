from juicer.utils import *

class ReiTerminalSpider(JuicerSpider):
    name = 'rei_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/product/')[-1]
        sk = sk.split('/')[0]
        item.set('sk', sk)
        item.textify('title', '//h1[@class="fn"]')
        item.textify('price', '//li[@itemprop="price"]')
        original_price = textify(hdoc.select('//li[@class="originalPrice"]//span'))
        if original_price:
            item.set('original_price', original_price)
        item_num = textify(hdoc.select('//p[@class="productSKU"]')).replace('Item #', ' ') or textify(hdoc.select('//p[@class="identifier productSKU"]')).replace('Item #', ' ')
        item.set('item_num', item_num)
        item.textify('img_url', '//div[@id="prodImg"]//a//img[@id="featuredImg"]/@src')
        review_count = textify(hdoc.select('//div[@id="prRead"]//a')).replace('Read ', '')
        review_count = review_count.replace(' Reviews', '')
        if review_count:
            item.set('review_count', review_count)
        item.textify('description', '//div[@class="tabArea1"]//ul//li')
        yield item.process()
