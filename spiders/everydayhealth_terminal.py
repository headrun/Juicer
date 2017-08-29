from juicer.utils import *

class EverydayhealthTerminalSpider(JuicerSpider):
    name = 'everydayhealth_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('-')[-1]
        item.set('sk', sk)
        item.textify('title', '//div[@class="top"]//h1')
        item.textify('doctor_name', '//div[@class="page-header"]')
        item.textify('doctor_specialty', '//div[contains(text(), "Speciality and Board Certification:")]//parent::div[@class="minisection"]//ul//li')
        item.textify('doctor_address', '//div[@class="location"]')
        item.textify('doctor_gender', '//span[contains(text(), "Gender:")]//parent::div[@class="minisection"]//span[not(contains(text(), "Gender:"))]')
        item.textify('doctor_education', '//div[contains(text(), "Education:")]//parent::div[@class="minisection"]//ul//li')
        item.textify('doctor_practise', '//div[contains(text(), "Practice Affiliations:")]//parent::div[@class="minisection"]//ul//li')
        item.textify('doctor_hospital', '//div[contains(text(), "Hospital affiliations:")]//parent::div[@class="minisection"]//ul//li')
        item.textify('doctor_practise', '//span[contains(text(), "Years in Practice: ")]//parent::div[@class="minisection"]//span[not(contains(text(), "Years in Practice: "))]')
        item.textify('doctor_language_in_office', '//div[contains(text(), "Languages Spoken in Office:")]//parent::div[@class="minisection"]//ul//li')
        yield item.process()
