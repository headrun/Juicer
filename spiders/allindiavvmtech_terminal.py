
from juicer.utils import *

class AllIndiaVVMtechTerminalSpider(JuicerSpider):
    name = 'allindiavvmtech_terminal'

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

        affliation = textify(hdoc.select('//table[@width="360"]//tr[1]//text()')).replace("Affiliated To","").replace("Photo Gallery","").replace("\r\n\t\t\t\t","")
        if affliation:
            item.set('affliation', affliation)

        college_type = textify(hdoc.select('//table[@width="360"]//tr[2]//text()')).replace("College Type", "") 
        if college_type:
            item.set('college_type', college_type)

        category = textify(hdoc.select('//table[@width="360"]//tr[3]//text()')).replace("Category", "") 
        if category:
            item.set('category', category)

        address = textify(hdoc.select('//table[@width="360"]//tr[4]//text()')).replace("\r\n\t\t\t\t", "").replace("Address", "").replace("View Map", "") 
        if address:
            item.set('address', address)

        map_image = textify(hdoc.select('//td[@valign="top"]/a/@href[contains(.,"viewmap")]'))
        if map_image:
            map_image = 'http://www.vidyavision.com/' + map_image
        item.set('map_image',map_image)

        location = textify(hdoc.select('//table[@width="360"]//tr[5]//text()')).replace("Location", "")
        if location:
            item.set('location', location)

        phone = textify(hdoc.select('//table[@width="360"]//tr[6]//text()')).replace("Phone", "").replace("\r\n\t\t\t\t","").replace("","")
        if phone:
            item.set('phone', phone)

        email = textify(hdoc.select('//table[@width="360"]//tr[7]//text()')).replace("Email", "").replace("-", "")
        if email:
            item.set('email', email)

        website_url = textify(hdoc.select('//table[@width="360"]//tr[8]//text()')).replace("Website","")
        if website_url:
            item.set('website_url', website_url)

        courses = []
        courses = textify(hdoc.select('//table[@width="360"]//tr[9]//text()')).replace("Courses","")
        if courses:
            item.set('courses', courses)

        specialisation = []
        specialisation = textify(hdoc.select('//td[@valign="top"]//div/text()')).replace("\r\n\t\t\t\t\t", "")
        if specialisation:
            item.set('specialisation',specialisation)

        yield item.process()

