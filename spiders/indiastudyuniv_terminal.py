
from juicer.utils import *

class IndiaStudyUnivTerminalSpider(JuicerSpider):
    name = 'indiastudyuniv_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        title = textify(hdoc.select('//table[@cellpadding="5"]//td[@valign="top"]//h1/text()'))
        item.set('title',title)

        address = textify(hdoc.select('//span[@id="ContentPlaceHolder1_lblAddress"]//text()'))
        item.set('address', address)

        city = textify(hdoc.select('//span[@id="ContentPlaceHolder1_lblCity"]//text()'))
        item.set('city', city)

        state = textify(hdoc.select('//span[@id="ContentPlaceHolder1_lblState"]//text()'))
        item.set('state', state)

        phone = []
        phone = textify(hdoc.select('//span[@id="ContentPlaceHolder1_lblPhoneNumber1"]//text()')).replace(":", "")
        item.set('phone', phone)

        email = textify(hdoc.select('//span[@id="ContentPlaceHolder1_lblEmail"]//text()'))
        item.set('email', email)

        website_url = textify(hdoc.select('//span[@id="ContentPlaceHolder1_lblHomePage"]//text()'))
        item.set('website_url', website_url)

        yield item.process()
