from juicer.utils import *

def gen_start_urls():
    items = lookup_items('99acres_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data


class AcresTerminalSpider(JuicerSpider):
    name = '99acres_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        price = textify(hdoc.select('//span[@class="b orng3"]//text()'))
        price_per_sq_feet = textify(hdoc.select('//div[contains (text(),"Price Per Unit:")]//text()'))
        propertydescription = textify(hdoc.select('//td[@class="f11"]/text()'))
      #  owner = textify(hdoc.select('//div[@class="m5 f12"]//div[@class="b"]//text()'))
        propertyname = textify(hdoc.select('//span[@class="f18 b hm5"]//text()'))
        property_address = textify(hdoc.select('//div[@class="hm5 floatl"]//text()'))
        additional_details =textify(hdoc.select('//div[contains(text(),"Additional Details")]//following-sibling::table//text()'))
        no_bath = textify(hdoc.select('//div[@class="info f12"]//table//tr//td[@class="sepl"]//table[@class="f12"]//text()'))
        built_up_area = textify(hdoc.select('//span[@id="builtupArea"]//text()'))
       # contactdetails = textify(hdoc.select('//div[@class="m5 f12"]//text()'))
        contactperson = textify(hdoc.select('//div[@class="m5 f12"]//div[@class="b"]//text()'))
        propertygroup = textify(hdoc.select('//div[@class="m5 f12"]/text()'))
        contactaddress = textify(hdoc.select('//div[@class="m5 f12"]//div[@class="mt10"][1]//text()'))
        website = textify(hdoc.select('//span[contains(text(),"Website")]//following-sibling::a/text()'))
        property_code = textify(hdoc.select('//div[@class="f12 mt10"]//text()'))
        additional_features = textify(hdoc.select('//div[@class="floatl w33"]//ul//li'))
        airport = textify(hdoc.select('//span[contains(text(),"Airport")]/parent::*/text()'))
        railway = textify(hdoc.select('//span[contains(text(),"Railway")]/parent::*/text()'))
        hospital = textify(hdoc.select('//span[contains(text(),"Hospital")]/parent::*/text()'))
        city_center = textify(hdoc.select('//span[contains(text(),"City Center")]/parent::*/text()'))
        school = textify(hdoc.select('//span[contains(text(),"School")]/parent::*/text()'))
        atm = textify(hdoc.select('//span[contains(text(),"ATM")]/parent::*/text()'))
        key_landmarks  = textify(hdoc.select('//span[contains(text(),"Key Landmarks")]/parent::*/text()'))
        sk = response.url
        ref_url = response.url
        item.set('sk', sk)
        item.set('Price',price)
        item.set('Price Per Sq Feet',price_per_sq_feet)
        item.set('Property Description',propertydescription)
       # item.set('Owner',owner)
        item.set('Property Address',property_address)
        item.set('Property Name',propertyname)
        item.set('Additional Details',additional_details)
        item.set('No_bath',no_bath)
        item.set('built_up_area',built_up_area)
       # item.set('Contact Details',contactdetails)
        item.set('Contact Person',contactperson)
        item.set('Property Group',propertygroup)
        item.set('Contact Address',contactaddress)
        item.set('Website',website)
        item.set('property_code',property_code)
        item.set('additional_features',additional_features)
        item.set('airport',airport)
        item.set('railway',railway)
        item.set('hospital',hospital)
        item.set('city_center',city_center)
        item.set('school',school)
        item.set('atm',atm)
        item.set('key_landmarks',key_landmarks)
        item.set('got_page', True)
        item.update_mode = 'custom'
        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and old_data['got_page'] == True:
            return old_data
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data


SPIDER = AcresTerminalSpider()



