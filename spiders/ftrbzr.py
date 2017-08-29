import re
from datetime import datetime
from juicer.utils import *

class Spider(JuicerSpider):
    name = "futurebazar"
    start_urls = ['http://www.futurebazaar.com/clothing-accessories/ch/920/?q=&min=99&max=27526&c=921&b=365&b=759&b=371&b=378&b=824&b=377&b=2&b=757&b=373&b=386&b=379&b=720&b=368&b=758&b=391&b=8', 'http://www.futurebazaar.com/clothing-accessories/ch/920/?q=&min=99&max=27526&c=931&b=365&b=759&b=371&b=378&b=824&b=377&b=2&b=757&b=373&b=386&b=379&b=720&b=368&b=758&b=391&', 'http://www.futurebazaar.com/clothing-accessories/ch/920/?q=&min=99&max=27526&c=942&b=365&b=759&b=371&b=378&b=824&b=377&b=2&b=757&b=373&b=386&b=379&b=720&b=368&b=758&b=3', 'http://www.futurebazaar.com/clothing-accessories/ch/920/?q=&min=99&max=27526&c=951&b=365&b=759&b=371&b=378&b=824&b=377&b=2&b=757&b=373&b=386&b=379&b=720&b=368&b=758&']

    def parse(self,response):
 #       pop = get_request_url(response).split('&page=')[-1]
        hdoc =  HTML(response)
#        yield Request(hdoc.select('//div[@class="greed_prod"]//h3//a/@href'),self.parse_first,response, meta={'pop':pop})
        yield Request(hdoc.select('//div[@class="greed_prod"]//h3//a/@href'),self.parse_first,response)
        yield Request(hdoc.select('//a[@title="Go next page"]/@href'),self.parse,response)

    def parse_first(self,response):
        hdoc =HTML(response)
        item = Item(response, HTML)
   #     pop = response.meta.get('pop')
        sk = get_request_url(response).split('/')[-1]
        discount = textify(hdoc.select('//div[@class="product_desc"]//span[@class="fb f15"]')).strip()
        discount = discount.split(' ')[-1]
        size = []
        nodes = hdoc.select('//select[@name="size"]//option')
        for node in nodes:
            sizes = textify(node.select('.'))
            size.append(sizes)
        item.textify('deal heading', '//div[@class="product_desc"]//h1')
        item.textify('deal value', '//span[@class="fs fb"]')
        item.textify('details', '//div[@class="product_desc_details"]//div[1]//div/text()')
        item.set('sk',sk)
        item.set('savings from site', discount)
        item.textify('deal price','//td[@class="f16 fb forange"]')
        item.set('size',size)
        item.textify('Company', '//div[@class="f12"]//a')
#        item.set('popularity',pop)
        yield item.process()


SPIDER = Spider()
