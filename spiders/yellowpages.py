import re
from juicer.utils import *

class Spider(JuicerSpider):
    name = "yellowpages"
    allowed_domains = ['yellowpages.com']
    start_urls = ['http://www.yellowpages.com/sitemap']

    def parse(self,response):
        hdoc = HTML(response)
        states = hdoc.select('//li[@class="state"]//h3//a/@href')
        for state in states:
            yield Request(state, self.parse_city, response)

    def parse_city(self, response):

        hdoc = HTML(response)
        cities = hdoc.select('//ul[@class="cities-list"]//li//a/@href')
        for city in cities:
            yield Request(city, self.parse_categories, response)

    def parse_categories(self, response):
        hdoc = HTML(response)
        data = response.url.split('/')[-1].split('-')
        city = data[0].upper()
        state = data[1].upper()
        categories = hdoc.select('//ul[@class="categories-list"]//li//a/@href')
        for category in categories:
            yield Request(category, self.parse_details, response, meta={'city': city, 'state': state})

    def parse_details(self, response):
        hdoc = HTML(response)
        city = response.meta.get('city')
        state = response.meta.get('state')
        nodes = hdoc.select('//div[@id="results"]//div[@id]//h3//a/@href')
        for node in nodes:
            yield Request(node, self.parse_details1, response, meta={'city': city, 'state': state})

        next_page = hdoc.select('//a[contains(text(),"Next")]/@href')
        if next_page:
            yield Request(next_page, self.parse_details, response)

    def parse_details1(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        merchant_name = textify(hdoc.select('//h1[@class="fn org"]//span'))
        if merchant_name:
            business_categories = []
            categories = hdoc.select('//dd[@class="category-links"]//span')
            for category in categories:
                business_categories.append(textify(category.select('.//a/text()')))
            timings = textify(hdoc.select('//dt[contains(text(),"Hours")]//following-sibling::dd[1]//text()'))
            payments= textify(hdoc.select('//dt[contains(text(),"Payment Types Accepted")]//following-sibling::dd[1]/text()'))
            payments = payments.split(',')
            phone_number = textify(hdoc.select('//p[@class="phone"]'))
            fax_number = textify(hdoc.select('//div[contains(text(),"Fax:")]/text()')).replace('Fax: ', '')
            city = response.meta.get('city')
            state = response.meta.get('state')
            street_address = textify(hdoc.select('//span[@class="street-address"]'))
            merchant_city = textify(hdoc.select('//span[@class="locality"]'))
            merchant_state = textify(hdoc.select('//span[@class="region"]'))
            zip_code = textify(hdoc.select('//span[@class="postal-code"]'))
            business_link = textify(hdoc.select('//div//a[contains(text(),"http://")]'))
            email = textify(hdoc.select('//a[contains(text(),"Email this business")]/@href')).replace('mailto:','')
            sk = response.url
            item.set('Merchant Name', merchant_name)
            item.set('Business Categories', business_categories)
            item.set('Business Timings', timings)
            item.set('Phone Number', phone_number)
            item.set('Fax Number', fax_number)
            item.set('City', city)
            item.set('State', state)
            item.set('sk', sk)
            item.set('Address', street_address)
            item.set('Merchant city', merchant_city)
            item.set('Merchant State', merchant_state)
            item.set('Zip Code', zip_code)
            item.set('Merchant Website', business_link)
            item.set('Credit Cards', payments)
            item.set('Email', email)
            yield item.process()
