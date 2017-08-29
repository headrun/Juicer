from juicer.utils import *
from datetime import datetime
import re

class Spider(JuicerSpider):

    name = "17life_deal"
    start_urls = ['http://www.17life.com/ppon/todaydeals.aspx']
    def parse(self, response):
        hdoc = HTML(response)

        if "RecentDeals" not in response.url:
            yield Request(hdoc.select('//div[contains(@id, "DealGood")]//div[@class="DealMainTitle"]//a/@href'),self.parse_details, response)
        else:
            yield Request(hdoc.select(''))

    def parse_details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        title = xcode(textify(hdoc.select('//div[@class="MaindealTitle"]/text()')))
        print "title>>>>>>>>>>>>>>>>>>>>>>>", title
        item.set('title', title)
        actual_price = textify(hdoc.select('//table[@id="DiscountPriceR"]//td[1]/text()')[-1])
        item.set('actual_price', actual_price)
        discount = textify(hdoc.select('//table[@id="DiscountPriceR"]//td[2]/text()')[-1])
        item.set('discount', discount)
        savings = textify(hdoc.select('//table[@id="DiscountPriceR"]//td[3]/text()')[-1])
        item.set('savings', savings)
        country = "taiwan"
        sk = response.url.split('bid=')[-1]
        item.set('sk', sk)
        address = textify(hdoc.select('//div[@id="Addressinner"][0]//li/text()')).encode('utf-8')
        item.set('address', address)
        description = xcode(textify(hdoc.select('//div[@class="MainDealProductName"]/text()')))
        print "description>>>>>>>>>>>>>>>>", description
        item.set('description', description)
        currency = "$"
        date = datetime.now()
        date = date.strftime("%d-%b-%Y")
        total_sold = textify(hdoc.select('//div[@id="TimeOpenBuy"]/text()'))
        if total_sold:
            total_sold = re.findall('(\d+)',total_sold)[0]
        else:
            total_sold = "SOLD_OUT"
        item.set('total_sold', total_sold)
        deal_price = textify(hdoc.select('//div[@id="Price"]/text()')).strip()
        item.set('deal_price', deal_price)

        yield item.process()
