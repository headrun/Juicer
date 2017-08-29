from juicer.utils import *
from datetime import datetime
import re



def X(data):
    try:
        return ''.join([chr(ord(x)) for x in data]).decode('utf8', 'ignore').encode('utf8')
    except ValueError:
        return data.encode('utf8')



class Spider(JuicerSpider):

    name = "groupon"

    start_urls = ['http://www.groupon.com/chicago/all','http://www.groupon.com/central-jersey/all']

    def parse(self, response):

        hdoc = HTML(response)

        if "central-jersey" in response.url:

            countries =  hdoc.select('//ul[@class="country"]//li[@class="country"]')
            for country in countries:

                nation = textify(country.select('.//a/text()'))
                yield Request(country.select('.//a/@href'),self.parse_country, response, meta = {'nation':nation})

        if "chicago" in response.url:
            canada_city_list = []
            canada_list = hdoc.select('//li[@class="canada"]//a/@href')

            for canada_city in canada_list:
                canada_city = textify(canada_city)
                if "groupon.ca" not in canada_city:
                    canada_city = canada_city.split('/all')[0].split('/')[-1]
                    canada_city_list.append(canada_city)

            yield Request(hdoc.select('//a[contains(@class, "G_event E-drawer_click")]/@href'),self.parse_first, response,meta = {"canada_list":canada_city_list})

    def parse_first(self, response):

        hdoc = HTML(response)
        item = Item(response, HTML)
        canada_city_list = response.meta.get('canada_list')

        yield Request(hdoc.select('//div[contains(@class, "three_up")]//div[@class="inner"]//a/@href | //div[contains(@class, "one_up")]//div[@class="inner"]//a/@href'),self.parse_details, response, meta = {'url': response.url,'canada_list':canada_city_list})

    def parse_details(self, response):

        hdoc = HTML(response)

        item = Item(response, HTML)

        if "www.groupon.ca" not in response.url:
            title = textify(hdoc.select('//div[@class="deal_title"]//h2//a')).encode('utf-8')
            deal_price = textify(hdoc.select('//div[@id="amount"]/text()'))
            actual_price = textify(hdoc.select('//div[@id="deal_discount"]//dl[not(contains(@class, "s"))]//dd/text()'))
            discount = textify(hdoc.select('//dl[@class="discount"]//dd/text()'))
            savings = textify(hdoc.select('//dl[@class="save"]//dd/text()'))
            total_sold = textify(hdoc.select('//tr[@class="sum"]//td//span/text()'))
            if len(total_sold) == 0:
                total_sold = "0"
            description = textify(hdoc.select('//div[@class="pitch_content"]//p/text() | //div[@class="pitch_content"]//p//a/text()')).encode('utf-8')
            deal_provider = textify(hdoc.select('//div[@class="merchant_name"]/text()'))
            address = textify(hdoc.select('//ul[@class="locations"]//div[@class="address"]//p/text()'))
            city = response.meta.get('url').split('/all')[0].split('.com/')[-1]
            currency = "$"
            city_list = textify(response.meta.get('canada_list'))
            if "montreal" in city:
                country = "canada"
            elif city in city_list:
                country = "canada"
            else:
                country = "U.S.A"
            sk = response.url.split('com/')[-1]
            deal_status = textify(hdoc.select('//div[@class="unavailable_deal_message sold_out"]//text()'))
            if "Sold Out" in deal_status:
                deal_type = "pastdeals"
                date = ""
            else:
                deal_type = "todaysdeals"
                date = datetime.now()
                date =date.strftime("%d-%m-%Y")


            item.set('title', title)
            item.set('description', description)
            item.set('date', date)
            item.set('deal_type', deal_type)
            item.set('sk', sk)
            item.set('country', country)
            item.set('city', city)
            item.set('deal_provider', deal_provider)
            item.set('address', address)
            item.set('deal_price', deal_price)
            item.set('total_sold', total_sold)
            item.set('currency', currency)
            item.set('actual_price', actual_price)
            item.set('savings', savings)
            item.set('discount', discount)

            yield item.process()


    def parse_country(self, response):
        hdoc = HTML(response)
        nation = response.meta.get('nation')
        item = Item(response, HTML)
        
        cities = hdoc.select('//div[@id="citySelectBox"]//ul//li')
        for city in cities:
            town = textify(city.select('.//a/text()'))
            yield Request(city.select('.//a/@href'),self.parse_city, response, meta = {'country': nation, 'city':town})



    def parse_city(self, response):
        hdoc = HTML(response)


        item = Item(response, HTML)

        title = textify(hdoc.select('//div[@id="contentDealTitle"]//h1//a/text()')).encode('utf-8')
        if len(title) ==0:
            title = textify(hdoc.select('//div[@id="contentDealTitle"]//h1/text()')).encode('utf-8')

        deal_price = textify(hdoc.select('//span[@class="price"]//span/text()')).encode('utf-8')
        currency = re.findall('\d+ (.*)',deal_price)
        if len(currency) != 0:
            currency = X(currency[-1])
        else:
            currency =  re.findall('(.*?)\d+',deal_price)
            if len(currency) != 0:
                currency = X(currency[0])
            else:
                currency = re.findall('(.*?) \d+',deal_price)
                if len(currency) != 0:
                    currency = X(currency[0])
                else:
                    currency = re.findall('\d+(.*)',deal_price)
                    if len(currency) != 0:
                        currency = X(currency[-1])
                    else:
                        currency = ""
        discount = hdoc.select('//table[@class="savings"]//td[contains(@class, "co")]/text()')
        if discount:
            discount = textify(discount[-1]).encode('utf-8')
            date = datetime.now()
            date = date.strftime('%d-%m-%Y')
        else:
            discount = ""
            date = ""
        savings = hdoc.select('//table[@class="savings"]//td[not(contains(@class, "co"))]/text()')
        if savings:
            savings = textify(savings[-1]).encode('utf-8')
        else:
            savings = ""
        total_sold = textify(hdoc.select('//span[@id="jDealSoldAmount"]/text()')).encode('utf-8')
        description = textify(hdoc.select('//div[@class="contentBoxNormalLeft"]//p/text()')).encode('utf-8')
        if len(description) == 0:
            description = textify(hdoc.select('//div[@class="contentBoxNormalLeft"]//div[contains(@style, "text")]/text()')).encode('utf-8')
        address = textify(hdoc.select('//div[@class="merchantContact"]//h2/following-sibling::text()')).encode('utf-8')
        country = response.meta.get('country').encode('utf-8')
        city = X(response.meta.get('city'))
        deal_provider = textify(hdoc.select('//div[@class="merchantContact"]//h2[@class="subHeadline"]/text()')).encode('utf-8')
        sk = response.url


        yield Request(hdoc.select('//div[contains(@class, "extraDealMulti")]//h3//a/@href'),self.parse_second, response, meta = {'country':country, 'city':city})
        yield Request(hdoc.select('//div[@class="linkArea"]//a[contains(@href, "missed")]/@href'),self.parse_second, response, meta = {'country':country, 'city':city})


        item.set('title', title)
        item.set('description', description)
        item.set('sk', sk) 
        item.set('country', country)
        item.set('city', city)
        item.set('date', date)
        item.set('deal_provider', deal_provider)
        item.set('address', address)
        item.set('deal_price', deal_price)
        item.set('total_sold', total_sold)
        item.set('currency', currency)
        item.set('savings', savings)
        item.set('discount', discount)

        yield item.process()



    def parse_second(self, response):

        hdoc = HTML(response)
        item = Item(response, HTML)

        if "missed" in response.url:
            city = response.meta.get('city')
            country = response.meta.get('country')
            yield Request(hdoc.select('//div[@class="recentDealDescription"]//a/@href'),self.parse_last, response, meta = {'country':country, 'city':city})
        else:

            title = textify(hdoc.select('//div[@id="contentDealTitle"]//h1//a/text()')).encode('utf-8')
            if len(title) ==0:
                title = textify(hdoc.select('//div[@id="contentDealTitle"]//h1/text()')).encode('utf-8')
            deal_price = textify(hdoc.select('//span[@class="price"]//span/text()')).encode('utf-8')
            currency = re.findall('\d+ (.*)',deal_price)
            if len(currency) != 0:
                currency = X(currency[-1])
            else:
                currency =  re.findall('(.*?)\d+',deal_price)
                if len(currency) != 0:
                    currency = X(currency[0])
                else:
                    currency = re.findall('(.*?) \d+',deal_price)
                    if len(currency) != 0:
                        currency = X(currency[0])
                    else:
                        currency = re.findall('\d+(.*)',deal_price)
                        if len(currency) != 0:
                            currency = X(currency[-1])
                        else:
                            currency = ""

            discount = hdoc.select('//table[@class="savings"]//td[contains(@class, "co")]/text()')
            if discount:
                discount = textify(discount[-1]).encode('utf-8')
            else:
                discount = ""
            savings = hdoc.select('//table[@class="savings"]//td[not(contains(@class, "co"))]/text()')
            if savings:
                savings = textify(savings[-1]).encode('utf-8')
                date = datetime.now()
                date = date.strftime('%d-%m-%Y')

            else:
                savings = ""
                date = ""
            total_sold = textify(hdoc.select('//span[@id="jDealSoldAmount"]/text()')).encode('utf-8')
            description = textify(hdoc.select('//div[@class="contentBoxNormalLeft"]//p/text()')).encode('utf-8')
            if len(description) == 0:
                description = textify(hdoc.select('//div[@class="contentBoxNormalLeft"]//div[contains(@style, "text")]/text()')).encode('utf-8')

            address = textify(hdoc.select('//div[@class="merchantContact"]//h2/following-sibling::text()')).encode('utf-8')
            deal_provider = textify(hdoc.select('//div[@class="merchantContact"]//h2[@class="subHeadline"]/text()')).encode('utf-8')
            sk = response.url
            country = response.meta.get('country').encode('utf-8')
            city = X(response.meta.get('city'))

            item.set('title', title)
            item.set('description', description)
            item.set('sk', sk)
            item.set('date', date)
            item.set('country', country)
            item.set('city', city)
            item.set('deal_provider', deal_provider)
            item.set('address', address)
            item.set('deal_price', deal_price)
            item.set('total_sold', total_sold)
            item.set('currency', currency)
            item.set('savings', savings)
            item.set('discount', discount)

            yield item.process()

    def parse_last(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        title = textify(hdoc.select('//div[@id="contentDealTitle"]//h1//a/text()')).encode('utf-8')
        if len(title) ==0:
            title = textify(hdoc.select('//div[@id="contentDealTitle"]//h1/text()')).encode('utf-8')

        deal_price = textify(hdoc.select('//span[@class="price"]//span/text()')).encode('utf-8')
        currency = re.findall('\d+ (.*)',deal_price)
        if len(currency) != 0:
            currency = X(currency[-1])
        else:
            currency =  re.findall('(.*?)\d+',deal_price)
            if len(currency) != 0:
                currency = X(currency[0])
            else:
                currency = re.findall('(.*?) \d+',deal_price)
                if len(currency) != 0:
                    currency = X(currency[0])
                else:
                    currency = re.findall('\d+(.*)',deal_price)
                    if len(currency) != 0:
                        currency = X(currency[-1])
                    else:
                        currency = ""

        discount = hdoc.select('//table[@class="savings"]//td[contains(@class, "co")]/text()')
        if discount:
            discount = textify(discount[-1]).encode('utf-8')
        else:
            discount = ""
        savings = hdoc.select('//table[@class="savings"]//td[not(contains(@class, "co"))]/text()')
        if savings:
            savings = textify(savings[-1]).encode('utf-8')
        else:
            savings = ""
        total_sold = textify(hdoc.select('//span[@id="jDealSoldAmount"]/text()')).encode('utf-8')
        description = textify(hdoc.select('//div[@class="contentBoxNormalLeft"]//p/text()')).encode('utf-8')
        if len(description) == 0:
            description = textify(hdoc.select('//div[@class="contentBoxNormalLeft"]//div[contains(@style, "text")]/text()')).encode('utf-8')

        address = textify(hdoc.select('//div[@class="merchantContact"]//h2/following-sibling::text()')).encode('utf-8')
        country = response.meta.get('country').encode('utf-8')
        city = X(response.meta.get('city'))
        deal_provider = textify(hdoc.select('//div[@class="merchantContact"]//h2[@class="subHeadline"]/text()')).encode('utf-8')
        sk = response.url
        deal_type = "pastdeals"

        item.set('title', title)
        item.set('description', description)
        item.set('sk', sk) 
        item.set('country', country)
        item.set('city', city)
        item.set('deal_provider', deal_provider)
        item.set('address', address)
        item.set('deal_price', deal_price)
        item.set('total_sold', total_sold)
        item.set('currency', currency)
        item.set('savings', savings)
        item.set('discount', discount)
        item.set('date', '')
        item.set('deal_type', deal_type)
        yield item.process()
