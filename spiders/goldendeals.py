from juicer.utils import *
from datetime import datetime


class Spider(JuicerSpider):
    name = "goldendeals"
    start_urls = ['http://www.goldendeals.rs/deals/belgrade/current','http://www.goldendeals.bg/deals/sofia/current','http://www.goldendeals.gr/deals/athens/current','http://www.goldendeals.ro/deals/bucharest/current']

    def parse(self, response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//li//a[@id="currentLink"]/@href | //li//a[@id="recentLink"]/@href'),self.parse_details, response)

    def parse_details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        if "recent" not in response.url:
            title = xcode(textify(hdoc.select('//h1[@class="noUnderline maintitle"]//span/following-sibling::a/text()')))
            deal_price = xcode(textify(hdoc.select('//a[@class="buttonBuy"]//span/text()')))
            actual_price = xcode(textify(hdoc.select('//ul[@class="offerCalculator"]//span[@class="price"]/text()')))
            discount = textify(hdoc.select('//span[@class="price"]//parent::li/following-sibling::li[not(contains(@class, "total"))]/span/text()'))
            savings = xcode(textify(hdoc.select('//ul[@class="offerCalculator"]//li[@class="total"]//span/text()')))
            total_sold = textify(hdoc.select('//h4/span/text()'))
            deal_provider = xcode(textify(hdoc.select('//address//span[@class="companyName"]/text()')))
            address = xcode(textify(hdoc.select('//address[not(contains(@class, "companyName"))]/text()')))
            date = datetime.now()
            date = date.strftime("%d-%m-%Y")
            sk = response.url
            description = xcode(textify(hdoc.select('//div[@class="containerRightBottom"]//p/text() | //div[@class="containerRightBottom"]//p//strong/text()')))

            if ".rs" in response.url:
                currency = "din"
                country = "serbia"
                city = "belgrade"
            elif ".gr" in response.url:
                currency = "euro"
                country = "Greece"
                city = "athens"
            elif ".bg" in response.url:
                currency = "Bulgarian lev"
                country = "Bulgaria"
                city = "sofia"
            elif ".ro" in response.url:
                currency = "Ron"
                country = "Romania"
                city = "bucharest"
                description = xcode(textify(hdoc.select('//div[@class="containerRightBottom"]//ul//div[@align="justify"]/text()')))
            deal_type = "todaysdeal"

            yield Request(hdoc.select('//div[@class="otherDeal"]//p//a/@href'), self.parse_details, response)

            item.set('title', title)
            item.set('description', description)
            item.set('deal_provider',deal_provider)
            item.set('actual_price', actual_price)
            item.set('discount',discount)
            item.set('savings', savings)
            item.set('deal_price',deal_price)
            item.set('date',date)
            item.set('currency', currency)
            item.set('country', country)
            item.set('sk', sk)
            item.set('deal_type', deal_type)
            item.set('address', address)
            item.set('total_sold', total_sold)
            item.set('city', city)

            yield item.process()

        else:
            nodes = hdoc.select('//div[@class="recentDealsBox"]')
            for node in nodes:
                date = textify(node.select('.//h3/text()'))
                yield Request(node.select('.//a/@href'),self.parse_last, response, meta = {'date':date})
            next_page = hdoc.select('//ul[@id="bottomNavigation"]')
            if next_page:
                yield Request(next_page.select('.//a/@href'),self.parse_details, response)

    def parse_last(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        title = xcode(textify(hdoc.select('//h1[@class="noUnderline maintitle"]//a/text()')))
        deal_price = xcode(textify(hdoc.select('//p[@class="buttonNoAvailableDeals"]//span/text()')))
        actual_price = xcode(textify(hdoc.select('//ul[@class="offerCalculator"]//span[@class="price"]/text()')))
        discount = xcode(textify(hdoc.select('//span[@class="price"]//parent::li/following-sibling::li[not(contains(@class, "total"))]/span/text()')))
        savings = xcode(textify(hdoc.select('//ul[@class="offerCalculator"]//li[@class="total"]//span/text()')))
        total_sold = xcode(textify(hdoc.select('//h4/span/text()')))
        deal_provider = xcode(textify(hdoc.select('//address//span[@class="companyName"]/text()')))
        address = xcode(textify(hdoc.select('//address[not(contains(@class, "companyName"))]/text()'))).strip()
        date =response.meta.get('date')
        sk = response.url
        if ".ro" not in response.url:
            desc = xcode(textify(hdoc.select('//div[@class="containerRightBottom"]//p/text()'))) or xcode(textify(hdoc.select('//div[@class="containerRightBottom"]//p//strong/text()')))
            print "desc>>>>>>>>>>>>>>>>>>>>>",desc
        if ".rs" in response.url:
            currency = "din"
            country = "serbia"
            city = "belgrade"
        elif ".gr" in response.url:
            currency = "euro"
            country = "Greece"
            city = "athens"
        elif ".bg" in response.url:
            currency = "Bulgarian lev"
            country = "Bulgaria"
            city = "sofia"
        elif ".ro" in response.url:
            currency = "Ron"
            country = "Romania"
            city = "bucharest"
            desc = xcode(textify(hdoc.select('//ul//div[@align="justify"]/text()| //ul//div[@align="justify"]//strong/text()')))
        deal_type = "pastdeals"


        item.set('title', title)
        item.set('description', desc)
        item.set('deal_provider',deal_provider)
        item.set('actual_price', actual_price)
        item.set('discount',discount)
        item.set('savings', savings)
        item.set('deal_price',deal_price)
        item.set('date',date)
        item.set('currency', currency)
        item.set('country', country)
        item.set('sk', sk)
        item.set('deal_type', deal_type)
        item.set('address', address)
        item.set('total_sold', total_sold)
        item.set('city', city)

        yield item.process()
