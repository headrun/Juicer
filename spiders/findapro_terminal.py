from juicer.utils import *

class FindaproTerminalSpider(JuicerSpider):
    name = 'findapro_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('-')[-1]
        item.set('sk', sk)
        item.textify('title', '//h1//span[@class="fn org"]')
        services = hdoc.select('//div[@class="service"]//span')
        services = [textify(s) for s in services]
        item.set('services', services)
        licenses = textify(hdoc.select('//div[@class="lic-info"]')).replace('amp;', '')
        licenses = licenses.split(',')
        item.set('licenses', licenses)
        profile_summary = textify(hdoc.select('//div[@class="pro-descr"]')).replace('Profile Summary', '')
        item.set('profile_summary', profile_summary)
        item.textify('locality', '//span[@class="locality"]')
        item.textify('region', '//span[@class="region"]')
        item.textify('zip_code', '//span[@class="postal-code"]')
        item.textify('phone_number', '//span[@class="tel"]')
        nodelist = hdoc.select('//div[@class="ri"]')
        reviews = []
        for node in nodelist:
            details = {}
            details['review_title'] = textify(node.select('.//h5//span'))
            details['review_description'] = textify(node.select('.//p[@class="descr"]'))
            details['reviewer'] = textify(node.select('.//table//td//span[@class="rev-user-name"]'))
            details['reviewer_location'] = textify(node.select('.//table//td//span[@class="rev-user-loc"]')).replace('from ', '')
            reviewer_count = textify(node.select('.//table//td//span[@class="rev-user-rev-count"]')).replace(' Review)', '')
            details['reviewer_count'] = reviewer_count.replace('(', '')
            review_date = textify(node.select('.//table//td[@class="right"]//div//span[@class="taken"]')).replace('Reviewed ', '')
            details['review_date'] = review_date
            reviews.append(details)
        if reviews:
            item.set('reviews', reviews)
            number_of_reviews = textify(hdoc.select('//div[@id="pro-details-nav"]//td//a//span')).replace('Recommendations (', '')
            number_of_reviews = number_of_reviews.replace(')', '')
            number_of_reviews = number_of_reviews.replace(' Photos', '')
            item.set('number_of_reviews', number_of_reviews)
        yield item.process()
