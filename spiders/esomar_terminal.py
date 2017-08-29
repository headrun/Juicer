from juicer.utils import *

class EsomarTerminalSpider(JuicerSpider):
    name = 'esomar_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('_')[0]
        item.set('sk', sk)
        company_name = textify(hdoc.select('//div[@id="centercontent"]/h2/text()[not(contains(., "Search for Companies"))][not(contains(., "Research conducted in:"))]'))
        item.set('company_name', company_name)
        address = textify(hdoc.select('//div[@id="rightcontent"]/text()')).split('Phone:')[0]
        item.set('address', address)
        phone_number = textify(hdoc.select('//div[@id="rightcontent"]/text()[contains(., "Phone:")]')).replace('Phone:', '')
        item.set('phone_number', phone_number)
        fax_number = textify(hdoc.select('//div[@id="rightcontent"]/text()[contains(., "Fax:")]')).replace('Fax:', '')
        item.set('fax_number', fax_number)
        email = textify(hdoc.select('//div[@id="rightcontent"]//a/@href[contains(., "@")]')).replace('mailto:', '')
        item.set('email', email)
        web = textify(hdoc.select('//div[@id="rightcontent"]//a[@target]/@href'))
        item.set('web', web)
        key_people = textify(hdoc.select('//div[@id="rightcontent"]/text()[contains(., "Mr.")]'))
        item.set('key_people', key_people)
        founded_year = xcode(textify(hdoc.select('//div[@id="rightcontent"]/text()[contains(., "Founded in")]'))).replace('Founded in:', '')
        founded_year = founded_year.replace('\xc2\xa0', '')
        item.set('founded_year', founded_year)
        employees = xcode(textify(hdoc.select('//div[@id="rightcontent"]/text()[contains(., "Employees")]'))).replace('Employees:', '')
        employees = employees.replace('\xc2\xa0', '')
        item.set('employees', employees)
        interviewers = xcode(textify(hdoc.select('//div[@id="rightcontent"]/text()[contains(., "Interviewers")]'))).replace('Interviewers:', '')
        interviewers = interviewers.replace('\xc2\xa0', '')
        item.set('interviewers', interviewers)
        turnover = xcode(textify(hdoc.select('//div[@id="rightcontent"]/text()[contains(., "Turnover")]'))).replace('Turnover:', '')
        turnover = turnover.replace('\xc2\xa0', '')
        item.set('turnover', turnover)
        yield item.process()
