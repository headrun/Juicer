from juicer.utils import *

class GolfNowTerminalSpider(JuicerSpider):
    name = 'golfnow_terminal'
    allow_domain = ['http://www.golfnow.com/']


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk) 

        title = textify(hdoc.select('//div[@class="courseDesc"]/h1'))
        item.set('title',title)

        desc = textify(hdoc.select('//div[@class="courseDesc"]/p')).strip()
        item.set('description',desc)

        course_notes = textify(hdoc.select('//td/p'))
        if course_notes:
            item.set('course_notes',course_notes)

        image_url = 'www.golfnow.com' + textify(hdoc.select('//div[@class="simage"]//img/@src'))
        item.set('image_url', image_url)

        amenities = hdoc.select('//div[@class="al"]')
        amenities = [textify(a).replace('amp;', '') for a in amenities]
        item.set('amenities', amenities)

        rules_list = hdoc.select('//div[@class="rulesList"]//div[@class="rules"]')
        rules_list = [textify(r) for r in rules_list]
        item.set('rules_list',rules_list)

        facility_information = {}
        key = hdoc.select('//div[@class="dtlSectionWrapper"][not(contains(@id, "ct"))]//td[@class="colLeft"]//strong')
        key = [textify(k).replace(':', '') for k in key]
        value = hdoc.select('//div[@class="dtlSectionWrapper"][not(contains(@id, "ct"))]//td[@class="colRight"]')
        value = [textify(v) for v in value]
        facility_information = dict(zip(key, value))
        item.set('facility_information', facility_information)

        information = {}
        key1 = hdoc.select('//div[@class="dtlSectionWrapper"][contains(@id, "ct")]//td[@class="colLeft"]//strong')
        key1 = [textify(k).replace(':', '') for k in key1]
        value1 = hdoc.select('//div[@class="dtlSectionWrapper"][contains(@id, "ct")]//td[@class="colRight"]')
        value1 = [textify(v) for v in value1]
        information = dict(zip(key1, value1))
        item.set('information', information)

        address_main = textify(hdoc.select('//div[@class="address"]/text()'))

        address = address_main.split('(')
        address1 = address[0].strip()
        item.set('address', address1)

        if ')' in address_main:
            phone_number = address_main.split('(')[1].strip()
            phone_number = '(' + phone_number
            if phone_number:
                item.set('phone_number', phone_number)

            if len(address)==3:
                tol_free = address_main.split('(')[2].strip()
                tol_free = '(' + tol_free
                if tol_free:
                    item.set('tol_free', tol_free)
        web_site = textify(hdoc.select('//div[@class="address"]/a/@href'))
        item.set('web_site', web_site)

        yield item.process()


