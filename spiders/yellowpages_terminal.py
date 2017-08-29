from juicer.utils import *

class YellowPagesTerminalSpider(JuicerSpider):
    name = 'yellowpages_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        merchant_name = textify(hdoc.select('//h1[@class="fn org"]//span'))
        if merchant_name:
            business_categories = []
            categories = hdoc.select('//dd[@class="category-links"]//span')
            for category in categories:
                business_categories.append(textify(category.select('.//a')))
            item.set('business_categories', business_categories)
            item.textify('timings', '//dt[contains(text(),"Hours")]//following-sibling::dd[1]//text()')
            payments= textify(hdoc.select('//dt[contains(text(),"Payment Types Accepted")]//following-sibling::dd[1]'))
            payments = payments.split(',')
            item.set('payments', payments)
            item.textify('phone_number', '//p[@class="phone"]')
            fax_number = textify(hdoc.select('//div[contains(text(),"Fax:")]')).replace('Fax: ', '')
            item.set('fax_number', fax_number)
            city = response.meta.get('city')
            state = response.meta.get('state')
            item.textify('street_address', '//span[@class="street-address"]')
            item.textify('merchant_city', '//span[@class="locality"]')
            item.textify('merchant_state', '//span[@class="region"]')
            item.textify('zip_code', '//span[@class="postal-code"]')
            item.textify('business_link', '//div//a[contains(text(),"http://")]')
            email = textify(hdoc.select('//a[contains(text(),"Email this business")]/@href')).replace('mailto:','')
            item.set('email', email)
            sk = get_request_url(response).split('=')[-1]
            item.set('sk', sk)
            yield item.process()
