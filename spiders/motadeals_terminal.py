from juicer.utils import *

class MotaDealsTerminalSpider(JuicerSpider):
    name = 'motadeals_terminal'
    allow_domain = ['slickdeals.net']

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = textify(hdoc.select('//div[@class="storeItemDesc"]/span')).replace('PRODUCT ID:', '').strip() 
        item.set('sk', sk) 

        title = textify(hdoc.select('//div[@class="storeItemDesc"]/h2'))
        item.set('title',title)

        product_id = textify(hdoc.select('//div[@class="storeItemDesc"]/span')).replace('PRODUCT ID:', '').strip()
        item.set('product_id', product_id)

        actual_price = textify(hdoc.select('//span[@class="old_price"]')).replace('Rs.','').strip()
        if actual_price:
            item.set('actual_price', int(actual_price))

        price = textify(hdoc.select('//p[@class="price"]/span[@class="final_price"]')).replace('Rs.','').strip()
        if price:
            item.set('price', int(price))

        features = hdoc.select('//ul[@class="high_list"]//li')
        features = [textify(r).replace('\t', '') for r in features]
        item.set('features', features)

        image_url = hdoc.select('//div[@class="product_thumb_list"]//img/@src')
        image_url = [textify(v) for v in image_url]
        item.set('image_url', image_url)

        description = xcode(textify(hdoc.select('//div[@class="storeItemDesc"]//p[not(contains(@class, "price"))]')))
        item.set('description', description)

        yield item.process()

 





