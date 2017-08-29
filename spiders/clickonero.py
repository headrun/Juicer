from juicer.utils import *
from datetime import datetime


class Spider(JuicerSpider):
    name = "clickonero"
    start_urls = ['http://www.clickonero.com.mx/static/recentdeals','http://www.clickonero.com.mx/deals/hoteles-viajes/v/all','http://www.clickonero.com.mx/deals/mexicodf/v/all','http://www.clickonero.com.mx/deals/guadalajara/v/all','http://www.clickonero.com.mx/deals/mexicodf-centro/v/all','http://www.clickonero.com.mx/deals/ofertas-nacionales/v/all','http://www.clickonero.com.mx/deals/monterrey/v/all','http://www.clickonero.com.mx/deals/puebla/v/all','http://www.clickonero.com.mx/deals/queretaro/v/all']

    def parse(self, response):

        hdoc = HTML(response)

        yield Request(hdoc.select('//div[@class="content_oferta_reciente"]//a[@class="link_promo_oferta"]/@href'), self.parse_details, response)

    def parse_details(self, response):

        item = Item(response, HTML)

        hdoc = HTML(response)

        title = textify(hdoc.select('//a[@class="main-deal-title-header-link"]/text()')).encode('utf-8')
        desc1 = hdoc.select('//div[@class="main-deal-description-specifics-info"]/p')
        if len(desc1) != 0:
            desc = textify(desc1.select('./text()')[0]).encode('utf-8')

            if len(desc) == 0:
                desc = textify(desc1.select('./text()')[1]).encode('utf-8')
        else:
            desc = textify(hdoc.select('//div[@class="main-deal-description-specifics-info"]/br/following-sibling::text()')[0]).strip().encode('utf-8')

        address = textify(hdoc.select('//span[@class="main-deal-sidebar-box-company-info-address"]/text()')).encode('utf-8')
        deal_price = hdoc.select('//div[@class="main-deal-sidebar-box-shop-price"]')
        if len(deal_price) != 0:
            deal_price = textify(deal_price.select('./text()'))
        else:
            deal_price = "deal Expired"

        sk = response.url.split('deals')[-1]
        sk = sk.split('/')[-1]
        if "hoteles-viajes" in sk:
            category = "hotel-travel deals"
            item.set('category', category) 
            city = "Mexico city"
        elif "mexicodf" in sk:
            city = "Mexico city"
        elif "guadalajara" in sk:
            city = "guadalajara"
        elif "mexicodf-centro" in sk:
            city = "Mexico city"
        elif "ofertas-nacionales" in sk:
            category = "national deals"
            city = "Mexico city"
        elif "monterrey" in sk:
            city = "monterrey"
        elif "puebla" in sk:
            city = "puebla"
        elif "queretaro" in sk:
            city = "queretaro"
        else:
            city = "Mexico city"

        currency = "$"

        past_deals = textify(hdoc.select('//span[@id="totalPurchases"][contains(@class, "null")]/text()'))

        if "final" in past_deals:
            category = "past deals"
            item.set('category', category)
            date = ""
            item.set('date',parse_date(date))
        else:
            date = datetime.now()
            date = date.strftime("%d-%m-%Y")
            item.set('date', parse_date(date))

        country = "Mexico"

        item.set('sk', sk)
        item.set('deal_price', deal_price)
        item.set('address', address)
        item.set('description', desc)
        item.set('title', title)
        item.set('city', city)
        item.set('currency', currency)
        item.textify('actual_value', '//div[@class="main-deal-sidebar-box-shop-numbers-value grey-style"]//span[@class="numbers-item"]/text()')
        item.textify('discount', '//div[@class="main-deal-sidebar-box-shop-numbers-discount grey-style"]//span[@class="numbers-item"]/text()')
        item.textify('saving', '//div[@class="main-deal-sidebar-box-shop-numbers-save grey-style"]//span[@class="numbers-item red-style"]/text()')
        item.textify('total_sold', '//div[@class="main-deal-sidebar-box-shop-amount-label"]//span[@id="totalPurchases"][not(contains(@class, "null"))]/text()')
        item.textify('deal_provider', '//h3[@class="main-deal-sidebar-box-company-info-name"]/text()')
        item.set('country', country)
        yield item.process()
