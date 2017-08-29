from juicer.utils import *

class QypeTerminalSpider(JuicerSpider):
    name = 'qype_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('-')[0]
        sk = sk.split('place/')[-1]
        item.set('sk',sk)
        item.textify('heading', '//h1[@class="fn org Black place-header__header"]')
        item.textify('ratings count', '//strong[@class="count"]')
        item.textify('short description', '//dd//p[@id="short_description"]')
        item.textify('long description', '//dd//p[@id="long_description"]')
        details = {}
        details['disabled access'] = textify(hdoc.select('//strong[contains(text(),"Disabled access:")]//parent::li'))
        details['best night'] = textify(hdoc.select('//strong[contains(text(),"Best night:")]//parent::li'))
        details['parking'] = textify(hdoc.select('//strong[contains(text(),"Parking:")]//parent::li'))
        details['air conditioning'] = textify(hdoc.select('//strong[contains(text(),"Air conditioning:")]//parent::li'))
        details['cloak room'] = textify(hdoc.select('//strong[contains(text(),"Cloak room:")]//parent::li'))
        details['private parties'] = textify(hdoc.select('//strong[contains(text(),"Private parties:")]//parent::li'))
        details['credit card accepted'] = textify(hdoc.select('//strong[contains(text(),"Credit cards accepted:")]//parent::li'))
        details['dress code'] = textify(hdoc.select('//strong[contains(text(),"Dress code:")]//parent::li'))
        details['price range'] = textify(hdoc.select('//strong[contains(text(),"Price range:")]//parent::li'))
        details['child friendly'] = textify(hdoc.select('//strong[contains(text(),"Child friendly:")]//parent::li'))
        item.set('details', details)
        item.textify('address', '//dd//p[@data-clicks="0"]')
        item.textify('img url', '//div[@class="MainPhotoInner"]//img/@src')
        item.textify('opening hours', '//dt[contains(text(),"Opening hours")]//following-sibling::dd')
        item.textify('special offer', '//div[@class="Coupon clearfix visible"]//p[@class="FS12"]')
        nodes = hdoc.select('//div[@class="ReviewBoxV2"]')
        # Reviews
        reviews = []
        for node in nodes:
            details = {}
            details['revw_title'] = textify(node.select('.//div[@class="PlaceReviewMeta"]'))
            details['revw_rating'] = textify(node.select('.//span[@class="rating"]'))
            details['revw_desc'] = textify(node.select('.//div[@class="ReviewTextV2"]//p'))
            details['revw_lovesthis'] = textify(node.select('.//p[@class="M0"]'))
            details['revw_num'] = textify(node.select('.//p[@class="PT2"]'))
            details['revw_name'] = textify(hdoc.select('.//div[@class="ContentUserPhotoBox"]//p//a'))
            reviews.append(details)
        item.set('reviews', reviews)
        yield item.process()
        got_page(self.name, response)
