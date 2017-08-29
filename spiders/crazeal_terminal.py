from juicer.utils import *

class CrazealTerminalSpider(JuicerSpider):
    name = 'crazeal_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk', sk)
        title = xcode(textify(hdoc.select('//h1/a'))) or xcode(textify(hdoc.select('//h1')))
        item.set('title', title)
        item.textify('image_url', '//div[@id="contentDealDescription"]//img/@src')
        price = xcode(textify(hdoc.select('//span[@class="price"]/span[@class="noWrap"]')))
        price = float(price.replace('\xe0\xa4\xb0', '').replace(',', ''))
        if price:
            item.set('price', int(price))
        discount = textify(hdoc.select('//tr[@class="row2"]/td[@class="col1"]')).strip().replace('%', '')
        if discount:
            item.set('discount', int(discount))
        savings = xcode(textify(hdoc.select('//tr[@class="row2"]/td[2]'))).strip()
        savings = float(savings.replace('\xe0\xa4\xb0', '').replace(',', ''))
        if savings:
            item.set('savings', int(savings))
        highlights = hdoc.select('//div[@class="viewHalfWidthSize"]//ul//li')
        highlights = [textify(h).replace('\r\n', '') for h in highlights]
        item.set('highlights', highlights)
        description = textify(hdoc.select('//div[@class="contentBoxNormalLeft"]//p')).strip()
        description = description.replace('\r\n', '')
        item.set('description', description)
        yield item.process()
