from juicer.utils import *

class HolidayrentalsTerminalSpider(JuicerSpider):
    name = 'holidayrentals_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)
        item.textify('title', '//span[@class="prevHeader"]//h1')
        price = textify(hdoc.select('//div[@class="rates"][1]//ul/li//span[not(contains(text(), "per week"))]'))
        price = ''.join(price.split())
        item.set('price', price)
        resort_type = textify(hdoc.select('//div[@id="summary-description"]/text()')).strip()
        item.set('resort_type', resort_type)
        locality = textify(hdoc.select('//span[contains(text(),"Location:")]/text()')).split('in')[-1]
        item.set('locality', locality)
        facilities = textify(hdoc.select('//div[@id="summary-amenities"]//ul//li//span/text()'))
        facility = textify(hdoc.select('//div[@id="summary-amenities"]//ul//li/text()'))
        facilities = facilities + ',' + facility
        item.set('facilities', facilities)
        item.textify('owner_ship', '//div[@id="summary-contact"]//p[1]//strong/text()')
        phone_number = textify(hdoc.select('//div[@id="contact-info"][@class="contact"]//p[contains(text(),"Telephone")]/text()')).replace('Telephone:','').strip()
        phone_number = ' '.join(phone_number.split())
        item.set('phone_number', phone_number)
        fax_number = textify(hdoc.select('//div[@id="summary-contact"]//p[contains(text(),"Fax:")]/text()')).replace('Fax:','').strip()
        item.set('fax_number', fax_number)
        item.textify('description', '//div[@class="prop-desc-txt"]//p/text()')
        item.textify('image_url', '//div[@class="photo-div"]//img/@src')
        details = hdoc.select('//div[@id="amenities-container"]//div[@class]')
        dt = {}
        for detail in details:
            a = textify(detail.select('.//span[@class="firstColumn"]/text()')).replace(':','')
            b = textify(detail.select('.//span[@class]//ul//li/text()'))
            b = ' '.join(b.split())
            if a:
                dt[a]=b
        item.set('details', dt)
        property_id = textify(response.url).split('/')[-1]
        property_id = re.findall(r'p(.*)',property_id)
        if property_id:
            property_id = property_id[0].split('.')[0]
            if '?' in property_id:
                property_id = re.findall('(.*)\?',property_id)
                if property_id:
                    property_id = property_id[0]
        item.set('property_id', property_id)
        yield item.process()
