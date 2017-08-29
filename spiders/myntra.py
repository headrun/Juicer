import re
from datetime import datetime

from juicer.utils import *


class Spider(JuicerSpider):
    name = "myntra"
    start_urls = ['http://www.myntra.com/kids', 'http://www.myntra.com/women', 'http://www.myntra.com/men']

    def parse(self,response):
        hdoc = HTML(response)
        deal = hdoc.select('//div[@class="product-listing clear mb10" ]//ul//li//a/@href')
        next_page = hdoc.select('//div[@class="pagination-links right"]//a/@href')
        yield Request(next_page, self.parse, response)
        yield Request(deal, self.details, response)

    def details(self,response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-2]
        if 'jersey' in response.url:
            sk = get_request_url(response)
        sizes = textify(hdoc.select('//div[@id="size-options"]//a')) or textify(hdoc.select('//select[@name="size"]//option[not(contains(text(), "Select"))]'))
        item.set('sizes', sizes)
        title = textify(hdoc.select('//div[@class="title-strip"]//h1')) or textify(hdoc.select('//div[@class="heading"]//h1'))
        item.set('title', title)
        jersy_type = textify(hdoc.select('//select[@id="tshirt-type"]//option'))
        item.set('jersy_type', jersy_type)
        actual_price = textify(hdoc.select('//span[@class="mrp"]//b')).replace('Rs ', '')
        item.set('actual_price', actual_price)
        description = textify(hdoc.select('//div[@class="product-description black-bg5 corners-bl-br"]//p')) or textify(hdoc.select('//div[@class="text-1"]/text()'))
        item.set('description', description)
        item.textify('specifications','//div[@class="product-description black-bg5 corners-bl-br"]//ul//li')
        item.textify('savings from site', '//div[@class="nav-buttons"]//div[@class="discount-label val"]//span')
        if hdoc.select('//span[@class="dis-price clearfix"]//strong'):
            price = textify(hdoc.select('//span[@class="dis-price clearfix"]//strong')).replace('Rs. ', '')
        elif hdoc.select('//span[@class="discount_dynamic"]//span[@class="product_price"]'):
            price = textify(hdoc.select('//span[@class="discount_dynamic"]//span[@class="product_price"]'))
        else:
            price = textify(hdoc.select('//span[@class="dis-price pt10 clearfix"]//strong')).replace('Rs. ', '')
        item.set('price', price)
        item.set('sk', sk)
        yield item.process()
