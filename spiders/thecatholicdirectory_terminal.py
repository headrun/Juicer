from juicer.utils import *

class TheCatholicDirectoryTerminalSpider(JuicerSpider):
    name = 'thecatholicdirectory_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('=')[-1]
        item.set('sk', sk)
        address = hdoc.select('//table//table//span[@class="PageTitleLight"][1]/../following-sibling::b/following-sibling::text()').extract()
        address = [re.sub(r'\s+', ' ', x) for x in address]
        address = [x.strip() for x in address if x.strip()]
        address = ', '.join(address)

        item = Item(response, HTML)
        title = textify(hdoc.select('//span[@itemprop="name"]//a')) or textify(hdoc.select('//span[@itemprop="name"]'))
        item.set('title', title)
        address = textify(hdoc.select('//div[@itemprop="address"]')).replace('\r\n\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t', '')
        item.set('address', address)
        mailing_address = textify(hdoc.select('//span[@itemprop="address"]/text()')).replace('\r\n\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t', '')
        item.set('mailing_address', mailing_address)
        item.textify('name', '//span[@itemprop="contactPoints"]')
        item.textify('phone_number', '//span[@itemprop="telephone"]')
        item.textify('fax_number', '//span[@itemprop="faxNumber"]')
        item.textify('website', '//a[@itemprop="url"]')
        item.textify('employees', '//span[@itemprop="employees"]')
        item.textify('rite', '//span[@itemprop="rite"]')
        item.textify('language', '//span[@itemprop="language"]')
        item.textify('primary_category', '//div[@id="breadcrumb"]//a[1]')
        item.textify('secondary_category', '//div[@id="breadcrumb"]//a[2]')
        item.textify('tertiary_category', '//div[@id="breadcrumb"]//a[last()]')

        yield item.process()
