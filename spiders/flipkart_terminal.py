#modified amazon_terminal.py to suit flipkart_terminal.py

from juicer.utils import *
import hashlib

def fill_book(hdoc):
    #Fillup all info for item, extract all info, store ina dictionary called data. return data
    data = {}
    data_detail = {}
    data['category'] = 'book'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    data['image_url'] = textify(hdoc.select('//div[@class="fk-content fksk-content"]/div[@class="fk-mproduct fk-mproduct-book"]//div[@id="mprodimg-id"]/img/@src'))
    data['summary'] = textify(hdoc.select('//div[@class="fk-content fksk-content"]/div[@class="fk-mproduct fk-mproduct-book"]//div[@id="description"]//div[@class="item_desc_text description line"]/text()'))
    details = hdoc.select('//div[@class="mprod-details"]//tr/td[contains(@class,"specs-key")]/parent::tr')
    for detail in details:
        detail_key = textify(detail.select('./td[@class="specs-key boldtext"]'))
        detail_value = textify(detail.select('./td[@class="specs-value"]'))
        data_detail[detail_key] = detail_value
    data['detail'] = data_detail
    return data

def fill_movie(hdoc):
    data = {}
    data_detail = {}
    lst_li = hdoc.select('//div[@class="mprod-details"]//li')
    data['category'] = 'movie'

    for item in lst_li:
        item_key = textify(item.select('.//div[@class="unit product_details_keys"]/text()'))
        item_value = textify(item.select('.//div[@class="lastUnit product_details_values"]'))

        data_detail[item_key] = item_value
    data['detail'] = data_detail

    data['summary'] = textify(hdoc.select('//div[@class="fk-content fksk-content"]//div[@id="description"]'))
    data['discount'] = textify(hdoc.select('//div[@class="price-table"]//span[@id="fk-mprod-discount-id"]/text()'))
    data['image_url'] = textify(hdoc.select('//div[@class="fk-mproduct fk-mproduct-movie"]//div[@id="mprodimg-id"]/img/@src'))

    return data

def fill_mobile(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'mobile'
    specs = hdoc.select('//div[@id="specifications"]//tr//td[@class="specs-key"]/parent::tr')
    for spec in specs:
        specs_key = textify(spec.select('./td[@class="specs-key"]'))
        specs_value = textify(spec.select('./td[@class="specs-value"]'))
        data_detail[specs_key] = specs_value
    data['detail'] = data_detail
    data['image_url'] = hdoc.select('//div[@id="main-image-id"]/div[@class="visible-image-small"]/img/@src')
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    data['summary'] = textify(hdoc.select('//div[@class="item_desc_text line"]'))

    return data

def fill_music(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'music'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]/h1'))
    data['summary'] = textify(hdoc.select('//div[@class="item_desc_text line"]'))
    details = hdoc.select('//div[@id="details"]//li')
    for detail in details:
        detail_key = textify(detail.select('./div[@class="unit product_details_keys"]'))
        detail_value = textify(detail.select('./div[@class="lastUnit product_details_values"]'))
        data_detail[detail_key] = detail_value
    data['detail'] = data_detail
    return data

def fill_game(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'game'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]/h1'))
    data['summary'] = textify(hdoc.select('//div[@class="item_desc_text line"]'))
    specs = hdoc.select('//div[@class="mprod-details"]//li/div[@class="unit product_details_keys"]/parent::li')
    for spec in specs:
        spec_key = textify(spec.select('./div[@class="unit product_details_keys"]'))
        spec_value = textify(spec.select('./div[@class=""lastUnit product_details_values]'))
        data_detail[spec_key] = spec_value
    data['detail'] = data_detail
    return data

def fill_camera(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'camera'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]/h1'))
    data['summary'] = textify(hdoc.select('//div[@id="description"]//div[@class="item_desc_text"]'))
    specs = hdoc.select('//div[@class="mprod-details"]//tr/th[@class="specs-key"]/parent::tr')
    for spec in specs:
        spec_key = textify(spec.select('./th[@class="specs-key"]'))
        spec_value = textify(spec.select('./td[@class="specs-value"]'))
        data_detail[spec_key] = spec_value
    data['detail'] = data_detail
    return data

def fill_computer(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'computer'
    data['title'] =  textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    specs = hdoc.select('//div[@class="mprod-details"]//tr/th[@class="specs-key"]/parent::tr')
    for spec in specs:
        spec_key = textify(spec.select('./th[@class="specs-key"]'))
        spec_value = textify(spec.select('./td[@class="specs-value"]'))
        data_detail[spec_key] = spec_value
    data['detail'] = data_detail
    return data

def fill_audioplayers(hdoc) :
    data = {}
    data_detail = {}
    data['category'] = 'audioplayer'
    data['title'] =  textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    data['summary'] = textify(hdoc.select('//div[@id="description"]'))
    specs = hdoc.select('//div[@class="mprod-details"]//tr/th[@class="specs-key"]/parent::tr')
    for spec in specs:
        spec_key = textify(spec.select('./th[@class="specs-key"]'))
        spec_value = textify(spec.select('./td[@class="specs-value"]'))
        data_detail[spec_key] = spec_value
    data['detail '] = data_detail
    return data

def fill_phcare(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'phcare'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    specs = hdoc.select('//div[@class="mprod-details"]//tr/th[@class="specs-key"]/parent::tr')
    for spec in specs:
        spec_key = textify(spec.select('./th[@class="specs-key"]'))
        spec_value = textify(spec.select('./td[@class="specs-value"]'))
        data_detail[spec_key] = spec_value
        data['detail'] = data_detail
    return data

def fill_homeapp(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'homeapp'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    specs = hdoc.select('//div[@class="mprod-details"]//tr/th[@class="specs-key"]/parent::tr')
    for spec in specs:
        spec_key = textify(spec.select('./th[@class="specs-key"]'))
        spec_value = textify(spec.select('./td[@class="specs-value"]'))
        data_detail[spec_key] = spec_value
        data['detail'] = data_detail
    return data

def fill_console(hdoc):
    data = {}
    data_detail = {}
    data['console'] = 'console'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    data['summary'] = textify(hdoc.select('//div[@class="mprod-details"]//div[@id="description"]'))
    specs = hdoc.select('//div[@class="mprod-details"]//li//div[@class="lastUnit product_details_values"]/parent::li')
    for spec in specs:
        spec_key = textify(spec.select('./div[@class="unit product_details_keys"]'))
        spec_value = textify(spec.select('./div[@class="lastUnit product_details_values"]'))
        data_detail[spec_key] = spec_value
    data['detail'] = data_detail
    return data

def fill_accessory(hdoc):
    data = {}
    data_detail = {}
    data['category'] = 'accessory'
    data['title'] = textify(hdoc.select('//div[@class="mprod-summary-title fksk-mprod-summary-title"]'))
    data ['image_url'] = textify(hdoc.select('//div[@class="mprodimg-section"]//img/@src'))
    specs = hdoc.select('//div[@class="mprod-details"]//tr/th[@class="specs-key"]/parent::tr')
    for spec in specs:
        spec_key = textify(spec.select('./th[@class="specs-key"]'))
        spec_value = textify(spec.select('./td[@class="specs-value"]'))
        data_detail[spec_key] = spec_value
    data['detail'] = data_detail
    return data

def fill_common_info(hdoc,data):
    reviews = []
    data['video_link'] = textify(hdoc.select('//div[@class="mprod-details"]//embed/@src'))
    lst_review = hdoc.select('//div[@class="review-list"]//div[@class="fk-review"]//div[@class="line bmargin10"]')
    for review_unit in lst_review:
       reviews.append( textify(review_unit))
    data['review'] = reviews
    data['price'] = textify(hdoc.select('//span[@class="price list price-td"]'))
    if data['price'] == '':
        data['price'] = textify(hdoc.select('//span[@class="price final-price our fksk-our"]'))
    data['discount'] = textify(hdoc.select('//div[@class="price-table"]//span[@id="fk-mprod-discount-id"]/text()'))
    
    return data


CALL_FOR_CATEGORY = {'book':fill_book,
                     'movie':fill_movie, 
                     'mobile':fill_mobile,
                     'music':fill_music,
                     'lgames':fill_game,
                     'lcameras':fill_camera,
                     'lcomputers':fill_computer,
                     'laudioplayers':fill_audioplayers,
                     'lphcare':fill_phcare,
                     'lhomeappliances':fill_homeapp,
                     'console':fill_console,
                     'accessory':fill_accessory
}

def gen_start_urls():
    
    items = lookup_items('flipkart_terminal', 'got_page:False', limit=2000)
    if not items:
        items = [(None, None, 'http://www.boattrader.com/browse/state')]
        empty_index(name, 'got_page:True')
    for _id, term, data in items:
        yield data

def get_sk(url, hdoc):
    sk = None
    if hdoc.select("//div[@class='fk-mprod-shipping-section-id']"):#Terminal Page
        sk = url.rsplit('?')[0]
    else: #Browse Page / Non-Terminal Page
        sk = hashlib.md5(url).hexdigest()

    return sk

def get_category(hdoc):
    '''
    Finds the category of the product, given the terminal page
    '''
    category = textify(hdoc.select('//div[@class="fk-content fksk-content"]/div[contains(@class,"fk-mproduct fk-mproduct-")]/@class'))
    category = category.split('-')[-1]

    return category

class FlipkartTerminalSpider(JuicerSpider):
    name = 'flipkart_terminal'
    allowed_domains = ['flipkart.com']
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        #we know all urls we get point to terminal pages
        item = Item(response, HTML)
        url = get_request_url(response)
        sk = get_sk(url, hdoc)

        if not sk:
            return

        # print '*'*150

        item.set('sk', sk)

        category = get_category(hdoc)

        data = CALL_FOR_CATEGORY.get(category, lambda hdoc: {})(hdoc)
        data = fill_common_info(hdoc, data)
        item.set('data', data)
        item.set('got_page', True)
        item.set('url', url)
        item.update_mode = 'custom'

        yield item.process()


    @staticmethod
    def _update_item(new_data, old_data):
        data = {}
        data.update(old_data)
        data.update(new_data)
        
        return data

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]

Spider = FlipkartTerminalSpider()

