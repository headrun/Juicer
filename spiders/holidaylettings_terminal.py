from juicer.utils import *

class HolidaylettingsTerminalSpider(JuicerSpider):
    name = 'holidaylettings_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)
        item.textify('title', '//h2[@class = "uh"][@id = "home_header"]')
        nodelist = hdoc.select('//table[@class="black"]//table//tr')
        summary = {}
        for node in nodelist:
            key = textify(node.select('.//th')).replace(':', '')
            value = textify(node.select('.//td//a')) or textify(node.select('.//td'))
            value = xcode(value)
            value = value.replace('\xc2\xa0', '')
            summary[key] = value
            key_1 = summary.keys()
            if "Slideshow" in key_1:
                summary.pop('Slideshow')
        item.set('summary', summary)
        item.textify('about_home', '//td[@id="content"]//p[2]')
        item.textify('image_url', '//img[@class="photo"]/@src')
        item.textify('activities', '//table[@class="black"]//p')
        nodes = hdoc.select('//table[@id="facilities"]//tr')
        facilities = {}
        for node in nodes:
            key = textify(node.select('.//th'))
            value = textify(node.select('.//td'))
            value = xcode(value)
            value = value.replace('\xc2\xa0', '')
            facilities[key] = value
        item.set('facilities', facilities)
        item.textify('rental_rates', '//td[contains(text(), "Rental prices originally quoted in: ")]//b')
        yield item.process()
