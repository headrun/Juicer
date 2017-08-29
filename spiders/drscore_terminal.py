from juicer.utils import *

class DrscoreTerminalSpider(JuicerSpider):
    name = 'drscore_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk', sk)
        item.textify('doctor_name', '//h1[@class="naming"]')
        item.textify('hospital', '//h2[@class="specialty_style"]')
        item.textify('about_doctor', '//p[@class="profile_desc"][1]')
        specialty = textify(hdoc.select('//strong[contains(text(), "Specialty:")]//parent::p/text()')).split(' ')[0]
        item.set('specialty', specialty)
        gender = textify(hdoc.select('//strong[contains(text(), "Specialty:")]//parent::p/text()')).split(' ')[-2]
        item.set('gender', gender)
        years_of_experience = textify(hdoc.select('//strong[contains(text(), "Specialty:")]//parent::p/text()')).split(' ')[-1]
        item.set('years_of_experience', years_of_experience)
        office_url = textify(hdoc.select('//a[contains(@name, "Office-Locations")]/@href'))
        yield Request(office_url, self.parse_office, response, meta={'item':item})

    def parse_office(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        office_address = textify(hdoc.select('//strong[contains(text(), "PRIMARY OFFICE LOCATION")]//parent::p')).replace('PRIMARY OFFICE LOCATION', '')
        office_address = office_address.split('Phone Number:')[0]
        item.set('office_address', office_address)
        phone_number = textify(hdoc.select('//strong[contains(text(), "PRIMARY OFFICE LOCATION")]//parent::p')).replace('PRIMARY OFFICE LOCATION', '')
        phone_number = phone_number.split('Phone Number:')[-1]
        item.set('phone_number', phone_number)
        yield item.process()
