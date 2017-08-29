import re
from datetime import datetime

from juicer.utils import *

class Spider(JuicerSpider):
    name = "yebhi"
    start_urls = ['http://www.yebhi.com/SH~0,523,0~0~1~-1~-1~-1~-1~op~/_Apparels.htm']

    def parse(self, response):
        hdoc = HTML(response)
        page = hdoc.select('//div[@class="search-item"]//a[@class="gotopage"]')
        if page:
            nodes = hdoc.select('//div[@class="search-item"]')
            for node in nodes:
                discount = textify(node.select('.//div[@class="offer"]'))
                if "100" in discount:
                    discount = 'none'
                yield Request(node.select('.//a[@class="gotopage"]/@href'),self.details, response,meta={'discount':discount})
            page_number = int(response.url.split('0~0~')[-1].split('~-')[0])
            if page:
                page_number = page_number + 1
                url = "http://www.yebhi.com/SH~0,523,0~0~%s~-1~-1~-1~-1~op~/_Apparels.htm" % str(page_number)
                yield Request(url,self.parse,response)

    def details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sizes = []
        nodes = hdoc.select('//select[@class="SizeDropDown"]//option')
        for node in nodes:
             sizes.append(textify(node.select('.')))
        sizes = sizes[1:]
        sk = get_request_url(response).split('/')[-3]
        discount = response.meta.get('discount')
        discount = discount.replace('\rOff',' ').strip()
        if "%" in discount:
            deal_price = textify(hdoc.select('//div[@class="price-detailsale"]//span'))
            deal_price = deal_price.split(':')[-1]
            actual_price = textify(hdoc.select('//div[@class="price-detailsale"]//strike'))
        else:
            deal_price = textify(hdoc.select('//div[@class="price-detail"]'))
            deal_price = deal_price.split(':')[-1]
            actual_price = ''
        overview = {}
        overview['category'] = textify(hdoc.select('//b[contains(text(),"Category:")]//ancestor::td//following-sibling::td'))
        overview['collars/neck'] = textify(hdoc.select('//b[contains(text(),"Collars/Neck:")]//ancestor::td//following-sibling::td'))
        overview['color'] = textify(hdoc.select('//b[contains(text(),"Color:")]//ancestor::td//following-sibling::td'))
        overview['departments'] = textify(hdoc.select('//b[contains(text(),"Departments:")]//ancestor::td//following-sibling::td'))
        overview['design'] = textify(hdoc.select('//b[contains(text(),"Design :")]//ancestor::td//following-sibling::td'))
        overview['fit'] = textify(hdoc.select('//b[contains(text(),"Fit:")]//ancestor::td//following-sibling::td'))
        overview['gender'] = textify(hdoc.select('//b[contains(text(),"Gender:")]//ancestor::td//following-sibling::td'))
        overview['material'] = textify(hdoc.select('//b[contains(text(),"Material:")]//ancestor::td//following-sibling::td'))
        overview['sleeves'] = textify(hdoc.select('//b[contains(text(),"Sleeves:")]//ancestor::td//following-sibling::td'))
        overview['usage'] = textify(hdoc.select('//b[contains(text(),"Usage:")]//ancestor::td//following-sibling::td'))
        overview['saree_desc'] = textify(hdoc.select('//b[contains(text(),"Blouse")]//ancestor::font[1]//following-sibling::font'))
        overview['style'] = textify(hdoc.select('//b[contains(text(),"Style:")]//ancestor::td//following-sibling::td'))

        item.textify('title', '//div[@class="product-desc"]')
        item.textify('company', '//div[@class="product-code"]')
        item.set('product value', actual_price)
        item.set('product price',deal_price)
        item.set('savings from site',discount)
        item.set('overview',overview)
        item.set('sizes',sizes)
        item.set('sk', sk)

        yield item.process()


