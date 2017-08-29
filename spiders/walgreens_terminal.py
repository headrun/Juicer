from juicer.utils import *

class WalgreensTerminalSpider(JuicerSpider):
    name = 'walgreens_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('ID=')[1]
        sk = sk.split('prod')[1][:-1]
        overview = textify(hdoc.select('//div[@class="vpd_overview"]//ul//li/text()')).split('\n\n\n')
        item.set('overview', overview)
        image_url = textify(hdoc.select('//div[@class="mrgTop20px txtCtrAlgn"]//img/@src')).split('\n\n\n')[0]
        item.set('image', image_url)
        item.textify('title', '//h1[@style="clear:both;"]')
        item.textify('product price', '//b[@id="price_amount"]')
        item.textify('availability', '//div[@class="float-left wid90"]//p//b')
        item.textify('description', '//div[@class="float-left padLt10px"]//ul[@class="description-list"]//li')
        item.textify('uses', '//div[@id="uses-content"]//p')
        item.textify('warnings', '//div[@id="warnings-content"]//li')
        ingrediants = textify(hdoc.select('//div[@class="float-left padLt10px"]//div[@id="ingredients-content"]//div')).replace('\n', '').replace('\t', '')
        item.set('ingrediants', ingrediants)
        yield item.set_many({'sk': sk, 'got_page': True}).process()
