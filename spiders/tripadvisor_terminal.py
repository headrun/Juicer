from juicer.utils import *

class TripadvisorTerminalSpider(JuicerSpider):
    name = 'tripadvisor_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('-d')[-1]
        sk = sk.split('-')[0]
        item.set('sk' , sk)
        item.textify('title', '//h1[@id="HEADING"]')
        street_address = textify(hdoc.select('//span[@rel="v:address"]//span[@class="street-address"]'))
        item.set('street_address', street_address)
        zip_code = textify(hdoc.select('//span[@rel="v:address"]//span[@property="v:postal-code"]'))
        item.set('zip_code', int(zip_code))
        locality = textify(hdoc.select('//span[@rel="v:address"]//span[@property="v:locality"]'))
        item.set('locality', locality)
        country = textify(hdoc.select('//span[@rel="v:address"]//span[@class="country-name"]'))
        item.set('country', country)
        rank = textify(hdoc.select('//div[@class="slim_ranking"]//text()')).split('#')[-1]
        item.set('rank', rank)
        reviews_count = int(textify(hdoc.select('//span[@property="v:count"]')).split(' ')[0])
        if reviews_count:
            item.set('reviews_count', reviews_count)
        image_url = hdoc.select('//div[@id="ICR2"]//img/@src[contains(., "tripadvisor")]')
        image_url = [textify(i) for i in image_url]
        item.set('image_url', image_url)
        ratings = {}
        excellent = textify(hdoc.select('//span[contains(text(),"Excellent")]//parent::label//parent::span//parent::div//span[@class="compositeCount"]'))
        if excellent:
            ratings['excellent'] = int(excellent)
        very_good = textify(hdoc.select('//span[contains(text(),"Very good")]//parent::label//parent::span//parent::div//span[@class="compositeCount"]'))
        if very_good:
            ratings['very_good'] = int(very_good)
        average = textify(hdoc.select('//span[contains(text(),"Average")]//parent::label//parent::span//parent::div//span[@class="compositeCount"]'))
        if average:
            ratings['average'] = int(average)
        poor = textify(hdoc.select('//span[contains(text(),"Poor")]//parent::label//parent::span//parent::div//span[@class="compositeCount"]'))
        if poor:
            ratings['poor'] = int(poor)
        terrible = textify(hdoc.select('//span[contains(text(),"Terrible")]//parent::label//parent::span//parent::div//span[@class="compositeCount"]'))
        if terrible:
            ratings['terrible'] = int(terrible)
        item.set('ratings', ratings)
        reviews = []
        nodes = hdoc.select('//div[@class="reviewSelector"]')
        for node in nodes:
            details = {}
            details['review_title'] = textify(node.select('.//div[@class="quote"]//a'))
            details['reviewer'] = textify(node.select('.//div[@class="username mo"]//span'))
            details['reviewer_location'] = textify(node.select('.//div[@class="member_info"]//div[@class="location"]'))
            reviewer_count = textify(node.select('.//div[@class="totalReviewBadge badge no_cpu"]//span[@class="badgeText"]')).split(' ')[0]
            if reviewer_count:
                details['reviewer_count'] = int(reviewer_count)
            details['review_description'] = textify(node.select('.//p[@class="partial_entry"]'))
            details['review_date'] = parse_date(textify(node.select('.//span[@class="ratingDate"]')).replace('Reviewed ', ''))
            reviews.append(details)
        item.set('reviews', reviews)
        yield item.process()
