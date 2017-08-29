from juicer.utils import *

class OwnersdirectTerminalSpider(JuicerSpider):
    name = 'ownersdirect_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('.htm')[0]
        got_page(self.name, response)
        item.textify('title', '//div[@id="content_top_property"]//span[@class="mainheadorange"]')
        item.textify('subs', '//div[@id="content_top_property"]//p[@class="textbluebold"]')
        item.textify('img_url', '//td[@align="center"]//img/@src')
        item.textify('description', '//p[@class="content_property_intro"]')
        item.textify('price_notes', '//span[contains(text(),"Notes on prices")]//parent::p/following-sibling::p[1]')
        item.textify('changeover_day', '//span[contains(text(),"Changeover day")]//parent::p/following-sibling::p[1]')
        item.textify('accomdation_notes', '//span[contains(text(),"Notes on accommodation")]//parent::p/following-sibling::p[1]')
        item.textify('animities/facilities', '//div[@class="palepanel_bl"]//ul//li')
        item.textify('accessibilities', '//span[contains(text(),"Accessibility")]//parent::p/following-sibling::p[1]')
        item.textify('outside', '//span[contains(text(), "Outside")]//parent::p/following-sibling::p[1]')
        item.textify('coast/beach', '//span[contains(text(),"Coast/Beach")]//parent::p/following-sibling::p[1]')
        item.textify('golf', '//span[contains(text(),"Golf")]//parent::p//following-sibling::p[1]')
        item.textify('skiing', '//span[contains(text(),"Skiing")]//parent::p//following-sibling::p[1]')
        item.textify('travel', '//span[contains(text(),"Travel")]//parent::p//following-sibling::p[1]')
        item.textify('distances', '//span[contains(text(),"Distances")]//parent::p//following-sibling::p[1]')
        item.textify('further_details', '//span[contains(text(),"Further details")]//parent::p//following-sibling::p[1]')
        item.textify('booking_notes', '//span[contains(text(),"Booking notes")]//parent::p//following-sibling::p[1]')
        item.textify('guest_comments', '//span[contains(text(),"Guest comments")]//parent::p/text()//following-sibling::p[1]')
        item.textify('about_owner', '//div[@class="profile"]//b[contains(text(),"About the owner")]//parent::p')
        yield item.process()
