from juicer.utils import *

def gen_start_urls():
    items = lookup_items('jcpenney_terminal', 'got_page:False', limit=1000)
    for _id, term, data in items:
        yield data

class JcpenneyTerminalSpider(JuicerSpider):
    name = 'jcpenney_terminal'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        saleprice = textify(hdoc.select('//div[@id="promotionMessage"]//font[@class="fSalePrice"]//text()'))
        originalprice = textify(hdoc.select('//div[@id="promotionMessage"]//font[@class="fOriginalPrice"]//text()'))
        currentprice = textify(hdoc.select('//div[@id="promotionMessage"]//font[@class="fCurrentPrice"]/text()'))
        tertiarycategory = textify(hdoc.select('//span[@id="BreadCrumbs_bcDataList_ctl02_bcSeparator"]//following-sibling::a/text()'))
        if 'back' in tertiarycategory:
            tertiarycategory = ""
        sk = get_request_url(response).split('&')[1]
        # k = response.url.split('&')[:2]
        # '&'.join(k)
        # sk = '&'.join(k)
        # ref_url = response.url
        item.set('sk', sk)
        item.textify('name','//div[@id="itemHeading"]')
        item.set('saleprice', saleprice)
        item.set('originalprice', originalprice)
        item.set('currentprice', currentprice)
        item.textify('description', '//div[@id="copyText"]')
        item.textify('image', '//div[@id="swfContent"]//img/@src')
        item.textify('primarycategory', '//span[@id="BreadCrumbs_bcDataList_ctl00_bcSeparator"]//following-sibling::a')
        item.textify('secondarycategory', '//span[@id="BreadCrumbs_bcDataList_ctl01_bcSeparator"]//following-sibling::a')
        item.set('tertiarycategory', tertiarycategory)
        item.textify('size', '//option[contains(text(),"Pick a size")]//following-sibling::option')
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


SPIDER = JcpenneyTerminalSpider()


