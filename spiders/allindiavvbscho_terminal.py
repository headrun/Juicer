
from juicer.utils import *

class AllIndiaVVBSchoTerminalSpider(JuicerSpider):
    name = 'allindiavvbscho_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('id=')[-1]
        item.set('sk', sk)

        logo = textify(hdoc.select('//td[@align="right"]/img[@height="70"]/@src'))
        if logo:
            logo = 'http://www.vidyavision.com/' + logo
        item.set('logo', logo)

        title = textify(hdoc.select('//td/h1/font/text()'))
        item.set('title',title)


        address = textify(hdoc.select('//table[@width="360"]//tr[1]//text()')).replace("\r\n\t\t\t\t", "").replace("Address", "").replace("View Map", "") 
        if address:
            item.set('address', address)

        map_image = textify(hdoc.select('//td[@valign="top"]/a/@href[contains(.,"viewmap")]'))
        if map_image:
            map_image = 'http://www.vidyavision.com/' + map_image
        item.set('map_image',map_image)

        location = textify(hdoc.select('//table[@width="360"]//tr[2]//text()')).replace("Location", "")
        if location:
            item.set('location', location)

        phone = textify(hdoc.select('//table[@width="360"]//tr[3]//text()')).replace("Phone", "").replace("\r\n\t\t\t\t","").replace("","")
        if phone:
            item.set('phone', phone)

        email = textify(hdoc.select('//table[@width="360"]//tr[4]//text()')).replace("Email", "").replace("-", "")
        if email:
            item.set('email', email)

        website_url = textify(hdoc.select('//table[@width="360"]//tr[5]//text()')).replace("Website","")
        if website_url:
            item.set('website_url', website_url)

        courses = []
        courses = textify(hdoc.select('//td[@valign="top"]//div/text()')).replace("Courses","")
        if courses:
            item.set('courses', courses)

        yield item.process()

