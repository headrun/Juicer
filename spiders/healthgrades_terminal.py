from juicer.utils import *

class HealthgradesTerminalSpider(JuicerSpider):
    name = 'healthgrades_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('-')[-1].replace('.cfm', '')
        item.set('sk', sk)
        item.textify('doctor_name', '//div[@id="physician-image-blurb"]//h3')
        item.textify('specialty', '//a[@id="Specialties1"]')
        item.textify('procedures_performed', '//ul[@id="procedures_wrapper"]//li')
        item.textify('organization_name', '//span[@class="organizational-name "]')
        item.textify('doctor_street_address', '//span[@class="street-address post-office-box"]')
        item.textify('doctor_locality', '//span[@class="locality"]')
        item.textify('doctor_region', '//span[@class="region"]')
        item.textify('poastal_code', '//span[@class="postal-code"]')
        gender = textify(hdoc.select('//div[@id="physicianGenderAge"]/text()')).split('\n')[0]
        item.set('gender', gender)
        age = textify(hdoc.select('//div[@id="physicianGenderAge"]/text()')).split('\n')[-1]
        item.set('age', age)
        year_from_graduation = textify(hdoc.select('//div[@id="yearsSinceGraduation"]/text()')).strip()
        item.set('year_from_graduation', year_from_graduation)
        conditions_treated = textify(hdoc.select('//ul[@id="conditions_treated_wrapper"]//li/text()')).strip()
        item.set('conditions_treated', conditions_treated)
        accepting_new_patients = textify(hdoc.select('//div[@class="section"]/text()')).strip()
        item.set('accepting_new_patients', accepting_new_patients)
        hospital_url = textify(hdoc.select('//h3//a[@class="white tab"]/@href[contains(., "/hospital-affiliations")]'))
        yield Request(hospital_url, self.parse_hospital, response, meta={'item':item})

    def parse_hospital(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        hospital_name = textify(hdoc.select('//div[@class="hosp_Name sectionBottom"]//a')).replace('Center ', 'Center ; ')
        item.set('hospital_name', hospital_name)
        hospital_address = textify(hdoc.select('//div[@class="hosp_address"]')).replace('( Map ) ', ' ; ')
        item.set('hospital_address', hospital_address)
        yield item.process()
