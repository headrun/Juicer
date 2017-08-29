from juicer.utils import *

class DealerdexTerminalSpider(JuicerSpider):
    name = 'dealerdex_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('+')[-1]
        item.set('sk', sk)
        item.textify('title', '//h1//span[@id="ctl00_ContentPlaceHolder1_lblDealer"]')
        item.textify('phone_number', '//h2//span[@id="ctl00_ContentPlaceHolder1_lblPhoneNo"]')
        street = textify(hdoc.select('//span[@id="ctl00_ContentPlaceHolder1_DealerInfoControl1_Repeater1_ctl00_StreetAddressLabel"]'))
        city = textify(hdoc.select('//span[@id="ctl00_ContentPlaceHolder1_DealerInfoControl1_Repeater1_ctl00_CityLabel"]'))
        address = street + ', ' +  city
        item.set('address', address)
        item.textify('website', '//a[@id="ctl00_ContentPlaceHolder1_DealerInfoControl1_Repeater1_ctl00_WebSiteUrlLabel"]')
        item.textify('franchises', '//strong[contains(text(), "Franchise(s): ")]//following-sibling::span')
        item.textify('dealer_information', '//span[@id="ctl00_ContentPlaceHolder1_DealerInfoBox1"]')
        yield item.process()
