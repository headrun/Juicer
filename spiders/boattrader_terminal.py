from juicer.utils import *

class BoatTraderTerminalSpider(JuicerSpider):
    name = 'boattrader_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response)
        title = get_request_url(response).split('listing/')[1]
        item.set('title', title)
        key = hdoc.select('//div[@class="featuresList"]//li//span[@class="itemKey"]/text()')
        value = hdoc.select('//div[@class="featuresList"]//li//span[@class="itemData capitalize"]/text()')
        key = [textify(k).replace(':', '') for k in key]
        value = [textify(v) for v in value]
        details = dict(zip(key, value))
        item.set('details', details)
        item.textify('description', ('//p[@class="listingDesc"]').strip())
        seller_info = textify(hdoc.select('//dl[@class="sellerDetails"]')).split('View Dealer Inventory')[0]
        item.set('seller info', seller_info)
        yield item.process()
