from juicer.utils import *

class AngieslistTerminalSpider(JuicerSpider):
    name = 'angieslist_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('-')[-1]
        sk = sk.replace('.aspx', '')
        item.set('sk', sk)

        item.textify('title', '//div[@id="tree-topleft"]//h1')

        phone_number = textify(hdoc.select('//p[@class="tree-contactinfo"]/text()')).split(' (')[-1]
        phone_number = '(' + phone_number
        item.set('phone_number', phone_number)

        a_address = textify(hdoc.select('//p[@class="tree-contactinfo"]/text()')).split(' (')[0]
        z_address = a_address.split(', ')[-1]
        region = z_address.split(' ')[0]
        item.set('region', region)
        zip_code = z_address.split(' ')[-1]
        item.set('zip_code', int(zip_code))

        address = a_address.split(', ')[0]
        item.set('address', address)

        item.textify('website', '//div[@id="tree-topleft"]//p//a[@rel="nofollow"]/@href')

        contact = textify(hdoc.select('//div[@id="tree-topleft"]//strong[contains(text(), "Contact:")]//parent::p')).replace('Contact:', '')
        item.set('contact', contact)

        business_description = textify(hdoc.select('//div[@id="tree-topleft"]//strong[contains(text(), "Business Description:")]//parent::p')).replace('Business Description:', '')
        item.set('business_description', business_description)

        services = hdoc.select('//div[@id="tree-topleft"]//strong[contains(text(), "Services:")]//parent::p//a')
        services = [textify(s) for s in services]
        item.set('services', services)

        service_links =  hdoc.select('//div[@id="tree-topleft"]//strong[contains(text(), "Services:")]//parent::p//a/@href')
        service_links = [textify(l) for l in service_links]
        item.set('service_links', service_links)

        service_area = textify(hdoc.select('//div[@id="tree-topleft"]//strong[contains(text(), "Services Area:")]//parent::p'))
        item.set('service_area', service_area)

        details = {}
        nodelist = hdoc.select('//div[@id="tree-profile-content-leftcol"]//p')
        for node in nodelist:
            key = textify(node.select('.//strong'))
            value = xcode(textify(node.select('./text()')))
            value = value.replace('\xc2\xa0', '')
            value = value.replace('|', ',')
            details[key] = value
        if details:
            item.set('details', details)

        yield item.process()
