from juicer.utils import *

class TruliaTerminalSpider(JuicerSpider):
    name = 'trulia_terminal'


    def parse(self,response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('-')[0]
        region = textify(hdoc.select('//h1[@class="address"]')).strip()
        region = region.split(' ')[-2]
        description = textify(hdoc.select('//div[@class="listing_description_module"]'))
        item.set('description', repr(description))
        item.textify('provided by', '//th[text()="Provided by:"]//following-sibling::td//a')
        item.textify('lot size', '//th[text()="Lot:"]//following-sibling::td')
        item.textify('mls/id', '//th[text()="MLS/ID:"]//following-sibling::td')
        item.textify('bathrooms', '//th[text()="Bathrooms:"]//following-sibling::td')
        item.textify('bedrooms', '//th[text()="Bedrooms:"]//following-sibling::td')
        item.textify('total views', '//th[text()="Total views:"]//following-sibling::td')
        item.textify('zip', '//th[text()="Zip:"]//following-sibling::td//a')
        item.textify('price', '//th[text()="Price:"]//following-sibling::td//div[@class="fleft"]')
        item.textify('property type', '//th[text()="Property type:"]//following-sibling::td')
        item.textify('nearby school', '//th[text()="Nearby School:"]//following-sibling::td')
        item.textify('year built', '//th[text()="Year built:"]//following-sibling::td')
        item.textify('size', '//th[text()="Size:"]//following-sibling::td')
        item.textify('agent', '//div[text()="Agent:"]//following-sibling::span[@class="bold"]//a')
        item.textify('broker', '//div[text()="Broker:"]//following-sibling::span')
        item.textify('img_url', '//td[@class="photo_valign"]//img/@src')
        yield item.set_many({'sk': sk, 'region': region, 'got_page': True}).process()


