
from juicer.utils import *

class VcsDataTerminalSpider(JuicerSpider):
    name = 'vcsdata_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        company_name = textify(hdoc.select('//table[@width="100%"]//tr[3]//text()')).replace(":", "").replace("Company Name", "")
        item.set('company_name', company_name)

        address = textify(hdoc.select('//table[@width="100%"]//tr[4]//text()')).replace(":", "").replace("Address", "")
        item.set('address',address)

        phone = textify(hdoc.select('//table[@width="100%"]//tr[5]//text()')).replace(":", "").replace("Phone No", "")
        item.set('phone', phone)

        website_url = textify(hdoc.select('//table[@width="100%"]//tr[6]//text()')).replace(":", "").replace("Website", "")
        item.set('website_url', website_url)

        city = textify(hdoc.select('//td[contains(text(), "City")]//following-sibling::td/text()')).replace(":", "").replace("City", "")
        item.set('city', city)

        industry = textify(hdoc.select('//td[contains(text(), "Industry")]//following-sibling::td/text()')).replace(":", "").replace("Industry", "")
        item.set('industry', industry)

        pincode = textify(hdoc.select('//td[contains(text(), "Pin Code")]//following-sibling::td/text()')).replace(":", "").replace("Pin Code", "")
        item.set('pincode', pincode)

        state = textify(hdoc.select('//td[contains(text(), "State")]//following-sibling::td/text()')).replace("State", "").replace(":", "")
        item.set('state', state)

        description = textify(hdoc.select('//table[@width="100%"]//tr//div[@align="justify"]/text()'))
        item.set('description',description)

        yield item.process()
