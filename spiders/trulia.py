import re
from datetime import datetime

from juicer.utils import *


class Spider(JuicerSpider):
    name = "trulia"
    start_urls = ["http://www.trulia.com/"]

    def parse(self,response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//div[@class="newsfeed_item clearfix"]//div[@class="fleft"]//a/@href'),self.terminal,response)

    def terminal(self,response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//div[@class="row_address_details clearfix"]//div[@class="address_section"]//a/@href'),self.details,response)
        yield Request(hdoc.select('//span[@class="pg_link_cur"]//following-sibling::a[@class="pg_link"][1]/@href'),self.terminal,response)

    def details(self,response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('-')[0]
        region = textify(hdoc.select('//h1[@class="address"]')).strip()
        region = region.split(' ')[-2]
        item.textify('description', '//div[@class="listing_description_module"]')
        item.textify('provided by', '//th[text()="Provided by:"]//following-sibling::td//a')
        item.textify('lot size', '//th[text()="Lot:"]//following-sibling::td')
        item.textify('mls/id', '//th[text()="MLS/ID:"]//following-sibling::td')
        item.set('sk',sk)
        item.textify('bathrooms', '//th[text()="Bathrooms:"]//following-sibling::td')
        item.textify('bedrooms', '//th[text()="Bedrooms:"]//following-sibling::td')
        item.textify('total views', '//th[text()="Total views:"]//following-sibling::td')
        item.textify('zip', '//th[text()="Zip:"]//following-sibling::td//a')
        item.textify('price', '//th[text()="Price:"]//following-sibling::td//div[@class="fleft"]')
        item.textify('property type', '//th[text()="Property type:"]//following-sibling::td')
        item.set('region', region)
        item.textify('nearby school', '//th[text()="Nearby School:"]//following-sibling::td')
        item.textify('year built', '//th[text()="Year built:"]//following-sibling::td')
        item.textify('size', '//th[text()="Size:"]//following-sibling::td')
        item.textify('agent', '//div[text()="Agent:"]//following-sibling::span[@class="bold"]//a')
        item.textify('broker', '//div[text()="Broker:"]//following-sibling::span')
        item.textify('img_url', '//td[@class="photo_valign"]//img/@src')
        yield item.process()

SPIDER = Spider()

