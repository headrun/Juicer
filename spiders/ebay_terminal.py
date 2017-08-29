from juicer.utils import *

def gen_start_urls():
    items = lookup_items('ebay_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data


class EbayTerminalSpider(JuicerSpider):
    name = 'ebay_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        # sk = response.url
        sk = get_request_url(response).split('/')[-1]
        sk = sk.split('?')[0]
        ref_url = response.url
        #image = textify(hdoc.select('//center//img/@src')).split(',')[0]
        item.set('sk', sk)
        item.textify('name', '//h1[@class="vi-it-itHd"]')
        item.textify('shortdescription', '//h2[@class="vi-it-itSbHd"]')
        item.textify('title', '//h1[@class="vi-is1-titleH1"]')
        item.textify('price', '//th[contains(text(),"Price")]//following-sibling::td//span//span')
        item.textify('originalprice', '//b[contains(text(),"Original price")]//parent::span')
        item.textify('discountedprice', '//b[contains(text(),"Discounted price")]//parent::span')
        item.textify('currentbid', '//th[contains(text(),"Current bid")]//following-sibling::td//span//span')
        item.textify('startingbid', '//th[contains(text(),"Starting bid")]//following-sibling::td//span//span')
        item.textify('winningbid', '//th[contains(text(),"Winning bid")]//following-sibling::td//span//span')
        item.textify('bidhistory', '//span[@class="vi-is1-s6"]//span//a[@rel="nofollow"]//span')
        item.textify('shipping', '//span[@id="fshippingCost"]')
        item.textify('delivery', '//div[@class="sh-TblCnt"]')
        item.textify('coverage', '//th[contains(text(),"Coverage")]//following-sibling::td//div')
        item.textify('returns', '//td[@class="vi-rpd-miyContent"]')
        item.textify('primarycategory', '//ul[@class="in"]//li[1]//a')
        item.textify('secondarycategory', '//ul[@class="in"]//li[2]//a')
        item.textify('tertiarycategory', '//ul[@class="in"]//li[3]//a')
        item.textify('sellerid', '//span[@class="mbg-nw"]')
        item.textify('sellerpositivefeedback', '//span[@class="s-gray z_a"]')
        item.textify('itemlocation', ('//td[contains(text(),"Item location")]//following-sibling::td','//th[contains(text(),"Item Location")]//following-sibling::td//span'))
        item.textify('shipsto', '//td[contains(text(),"Ships to")]//following-sibling::td')
        item.textify('sellsto', '//td[contains(text(),"Sells to")]//following-sibling::td')
        #item.textify('image', '//center//img/@src').split(',')[0]
        item.textify('image', '//td[@class="vs_w-a"]//img/@src')
        item.textify('history', '//td[contains(text(),"History")]//following-sibling::td//a')
        item.textify('payments', ('//div[@id="payDet1"]', '//th[contains(text(),"Payment")]//following-sibling::td//div/text()'))
        item.textify('itemnumber', '//td[contains(text(),"Item number:")]//following-sibling::td')
        item.textify('itemcondition', '//td[contains(text(),"Item condition")]//following-sibling::td')
        item.set('got_page', True)
        item.update_mode = 'custom'
        yield item.process()


    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

    @staticmethod
    def _update_item(new_data, old_data):
        if 'got_page' in old_data and 'got_page' not in new_data:
            new_data['got_page'] = old_data['got_page']

        data = {}
        data.update(old_data)
        data.update(new_data)
        return data


SPIDER = EbayTerminalSpider()

