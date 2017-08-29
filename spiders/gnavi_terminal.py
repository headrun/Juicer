from juicer.utils import *

class GnaviTerminalSpider(JuicerSpider):
    name = 'gnavi_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('.jp/')[-1]
        sk = sk.split('/')[0]
        item.set('sk', sk)
        title = textify(hdoc.select('//h1[@class="jp"]'))
        item.set('title', xcode(title))
        image_url = textify(hdoc.select('//td[@class="view"]//img/@src')) or textify(hdoc.select('//div[@id="figure"]//p//img/@src'))
        item.set('image_url', image_url)
        item.textify('category', '//th[contains(text(),"Category")]//following-sibling::td')
        item.textify('address', '//th[contains(text(),"Address")]//following-sibling::td//var')
        item.textify('access', '//th[contains(text(),"Access")]//following-sibling::td//var')
        item.textify('open', '//th[contains(text(),"OPEN")]//following-sibling::td//var/text()')
        item.textify('close', '//th[contains(text(),"CLOSE")]//following-sibling::td')
        item.textify('phone', '//th[contains(text(),"Phone")]//following-sibling::td//var')
        item.textify('average_price', '//th[contains(text(),"Average price")]//following-sibling::td//ul//li/var')
        item.textify('service_charge', '//th[contains(text(),"Service charge")]//following-sibling::td//var')
        item.textify('cover_charge', '//th[contains(text(),"Cover charge")]//following-sibling::td/text()')
        item.textify('cards_accepted', '//th[contains(text(),"Cards accepted")]//following-sibling::td//ul')
        item.textify('languages', '//th[contains(text(),"Languages")]//following-sibling::td//ul')
        item.textify('eat_menu', '//th[contains(text(),"All-you-can-eat menu")]//following-sibling::td//ul')
        item.textify('drink_menu', '//th[contains(text(),"All-you-can-drink menu")]//following-sibling::td//ul')
        item.textify('smoking_prohibition', '//th[contains(text(),"Prohibitions on smoking")]//following-sibling::td//ul')
        item.textify('children', '//th[contains(text(),"Children")]//following-sibling::td//ul//li')
        item.textify('pets', '//th[contains(text(),"Pets")]//following-sibling::td//ul')
        item.textify('barrier_free', '//th[contains(text(),"Barrier-free")]//following-sibling::td//ul')
        item.textify('seating_capacity', '//th[contains(text(),"Seating capacity")]//following-sibling::td')
        yield item.process()
        got_page(self.name, response)
