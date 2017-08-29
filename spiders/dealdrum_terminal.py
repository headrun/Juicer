from juicer.utils import *

class DealdrumTerminalSpider(JuicerSpider):
    name = 'dealdrum_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)

        title =  textify(hdoc.select('//div[@class="title"]//a/text()'))
        item.set('title', title)

        actual_price = textify(hdoc.select('//div[@class="a12"]//div[contains(text(), "Value")]//span[@class="a18"]/text()'))
        if actual_price:
            item.set('actual_price', int(actual_price))

        price = textify(hdoc.select('//div[@class="a12"]//div[contains(text(), "You pay")]//span[@class="a18"]/text()')).strip()
        if price:
            item.set('price', int(price))

        discount = textify(hdoc.select('//div[contains(text(), "Discount")]//span[@class="a18"]')).replace('%', '')
        if discount:
            item.set('discount', int(discount))

        root = textify(hdoc.select('//div[@class="main-deal-discount"]//span'))
        if 'off' in root:
            discount = root.replace('% off','')
            item.set('discount', int(discount))

        else:
            advance_payment = root.replace('Rs.', '').strip()
            item.set('advance_payment', int(advance_payment))

        image_url = textify(hdoc.select('//div[contains(@style, "width: 440px;")]//img/@src'))
        image_url = get_request_url(response).split('.com/')[0] + '.com' + image_url
        item.set('image_url', image_url)

        address = xcode(textify(hdoc.select('//div[@class="block-border"]//div[@id="addrs"]//div[@class="a12"]//text()'))).replace('\x96', '').strip()
        item.set('address', address)

        features = textify(hdoc.select('//div[@class="a12"]//ul//text()')).strip()
        item.set('features', features)

        description = textify(hdoc.select('//div[contains(@style, "float: right")]//div[@class="a12"][contains(@style, "margin")]//text()')).strip()
        item.set('description', description)

        merchants_info = xcode(textify(hdoc.select('//div[@id="details"]//div[@class="a12"]//text()'))).replace('\x96', '').strip()
        item.set('merchants_info', merchants_info)

        yield item.process()
