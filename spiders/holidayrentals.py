import re
from juicer.utils import *
import datetime

class Spider(JuicerSpider):
    name = "holidayrentals"

    start_urls = ['http://www.holiday-rentals.co.uk/World/r1.htm']

    def parse(self,response):
        hdoc = HTML(response)
        countries = hdoc.select('//div[@class="content"]//li//a/@href')
        for country in countries:
            yield Request(country, self.parse_state, response)

    def parse_state(self, response):
        hdoc = HTML(response)
        region = textify(hdoc.select('//div[@class="node-name-off"]/text()'))
        states = hdoc.select('//div[@class="content"]//li//a/@href')
        for state in states:
            yield Request(state, self.parse_hotels, response,meta={'region': region})

    def parse_hotels(self, response):
        hdoc = HTML(response)
        region = response.meta.get('region')
        area = textify(hdoc.select('//div[@class="node-name-off"]/text()'))
        hotels = hdoc.select('//a[@class="button-base micro mild"]/@href')
        for hotel in hotels[:3]:
            yield Request(hotel, self.parse_details, response, meta={'region': region, 'area': area})

        next_url = textify(hdoc.select('//a[contains(text(),"Next")]/@href'))
        if next_url:
            next_url = next_url.split(' ')[0]
            yield Request(next_url, self.parse_hotels, response, meta={'area': area})

    def parse_details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        region = response.meta.get('region')
        location = response.meta.get('area')

        title = textify(hdoc.select('//span[@class="prevHeader"]//h1/text()'))

        price = textify(hdoc.select('//div[@class="rates"][1]//ul/li//span/text()'))
        price = ''.join(price.split())

        resort_type = textify(hdoc.select('//div[@id="summary-description"]/text()')).strip()

        locality = textify(hdoc.select('//span[contains(text(),"Location:")]/text()')).split('in')[-1]

        facilities = textify(hdoc.select('//div[@id="summary-amenities"]//ul//li//span/text()'))
        facility = textify(hdoc.select('//div[@id="summary-amenities"]//ul//li/text()'))
        facilities = facilities + ',' + facility

        owner_ship = textify(hdoc.select('//div[@id="summary-contact"]//p[1]//strong/text()'))
        phone_number = textify(hdoc.select('//div[@id="contact-info"][@class="contact"]//p[contains(text(),"Telephone")]/text()')).replace('Telephone:','').strip()
        phone_number = ' '.join(phone_number.split())

        fax_number = textify(hdoc.select('//div[@id="summary-contact"]//p[contains(text(),"Fax:")]/text()')).replace('Fax:','').strip()

        description = textify(hdoc.select('//div[@class="prop-desc-txt"]//p/text()'))

        property_id = textify(response.url).split('/')[-1]
        property_id = re.findall(r'p(.*)',property_id)
        if property_id:
            property_id = property_id[0].split('.')[0]
            if '?' in property_id:
                property_id = re.findall('(.*)\?',property_id)
                if property_id:
                    property_id = property_id[0]

        details = hdoc.select('//div[@id="amenities-container"]//div[@class]')
        dt = {}
        for detail in details:
            a = textify(detail.select('.//span[@class="firstColumn"]/text()')).replace(':','')
            b = textify(detail.select('.//span[@class]//ul//li/text()'))
            b = ' '.join(b.split())
            if a:
                dt[a]=b

        sk = textify(response.url).split('/')[-1]

        item.set('title', title)
        item.set('price', price)
        item.set('owner_ship',owner_ship)
        item.set('facilities_size',facilities)
        item.set('locality', locality)
        item.set('description', description)
        item.set('details', dt)
        item.set('region', region)
        item.set('sk', sk)
        item.set('resort_type', resort_type)
        item.set('location', location)
        item.set('phone_number', phone_number)
        item.set('fax_number', fax_number)
        item.set('property_id', property_id)
        yield item.process()
