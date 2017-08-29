from juicer.utils import *

class Spider(JuicerSpider):
    start_urls = ['http://www.thecatholicdirectory.com/']
    name = 'thecatholicdirectory'

    def parse(self, response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//a[contains(@href, "directory.cfm?fuseaction=show_state&country=US&state=")]/@href'), self.parse_state, response)

    def parse_state(self, response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//a[contains(@href, "&absolutecity=")]/@href'), self.parse_city, response)

    def parse_city(self, response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//a[contains(@href, "directory.cfm?fuseaction=display_site_info&siteid=")]/@href'), self.parse_church, response)

    def parse_church(self, response):
        hdoc = HTML(response)
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
        item.textify('phone', '//span[@itemprop="telephone"]')
        item.textify('fax', '//span[@itemprop="faxNumber"]')
        item.textify('website', '//a[@itemprop="url"]')
        item.textify('employees', '//span[@itemprop="employees"]')
        item.textify('rite', '//span[@itemprop="rite"]')
        item.textify('language', '//span[@itemprop="language"]')
        item.textify('primary_category', '//div[@id="breadcrumb"]//a[1]')
        item.textify('secondary_category', '//div[@id="breadcrumb"]//a[2]')
        item.textify('tertiary_category', '//div[@id="breadcrumb"]//a[last()]')
        item.set('sk', response.url.split('=')[-1])

        yield item.process()
