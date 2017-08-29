from juicer.utils import *

class ServicemagicTerminalSpider(JuicerSpider):
    name = 'servicemagic_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('.')[-2]
        item.set('sk', sk)

        item.textify('title', '//a[@class="url"]//span[@class="fn org"]')
        phone_number = textify(hdoc.select('//div[@class="tel"]')).split(' ')[0]
        item.set('phone_number', phone_number)

        item.textify('street_address', '//span[@class="street-address"]')
        item.textify('locality', '//div[@class="adr"]//div//span[@class="locality"]', lambda y: y.split(',')[0])
        item.textify('region', '//div[@class="adr"]//div//span[@class="locality"]', lambda z: z.split(',')[-1].split(' ')[-2])
        zip_code = textify(hdoc.select('//div[@class="adr"]//div//span[@class="locality"]')).split(',')[-1]
        zip_code = zip_code.split(' ')[-1]
        item.set('zip_code', int(zip_code))

        services = []
        nodes = hdoc.select('//ul[@id="xmp-services-list"]/li')
        for node in nodes:
            cat = []
            sub_cat = []
            main_catogery = node.select('./@class')
            catogery = textify(node.select('./a'))
            if main_catogery:
                ping = node.select('.//ul//li//a')
                for s in ping:
                    sub_cat.append(textify(s))
            cat.append(catogery)
            cat.append(sub_cat)
            services.append(cat)
        item.set('services', services)

        item.textify('description', '//div[@class="fn org summary"]')
        business_since = textify(hdoc.select('//b[contains(text(), "In Business Since")]//parent::div')).replace('In Business Since ', '')
        item.set('business_since', int(business_since))

        provides_service = textify(hdoc.select('//b[contains(text(), "Provides Service To")]//parent::div')).replace('Provides Service To', '')
        provides_service = provides_service.replace('See All', '').strip()
        provides_service = provides_service.split(',')
        item.set('provides_service_to', provides_service)

        item.textify('quick_facts', '//b[contains(text(), "Other Quick Facts")]//parent::div//ul//li')
        membership_affliation = hdoc.select('//b[contains(text(), "Memberships & Affiliations")]//parent::div//ul//li')
        membership_affliation = [textify(m) for m in membership_affliation]
        item.set('membership_affliation', membership_affliation)

        business_hours = hdoc.select('//b[contains(text(), "Typical Business Hours")]//parent::div')
        business_hours = [textify(b).replace('Typical Business Hours (Please call to confirm)', '').strip() for b in business_hours]
        item.set('business_hours', business_hours)

        area_expertise = hdoc.select('//b[contains(text(), "Areas of Expertise")]//parent::div//ul//li')
        area_expertise = [textify(a) for a in area_expertise]
        item.set('area_expertise', area_expertise)

        product_brands_used = textify(hdoc.select('//b[contains(text(), "Product Brands Used")]//parent::div')).replace('Product Brands Used', '')
        product_brands_used = product_brands_used.replace('See All', '').replace('amp;', '').strip()
        product_brands_used = product_brands_used.split(',')
        item.set('product_brands_used', product_brands_used)

        state_license = {}
        keys = hdoc.select('//b[contains(text(), "State Licensing")]//parent::div//table[@class="about-profile-details-table"]//thead//td')
        keys = [textify(k).replace('#', '') for k in keys]
        values = hdoc.select('//b[contains(text(), "State Licensing")]//parent::div//table[@class="about-profile-details-table"]//thead//following-sibling::tr//td')
        values = [textify(v) for v in values]
        state_license = dict(zip(keys, values))
        item.set('state_license', state_license)

        insurance_carried = {}
        keys1 = hdoc.select('//b[contains(text(), "Insurance Carried")]//parent::div//table[@class="about-profile-details-table"]//thead//td')
        keys1 = [textify(k).replace('#', '') for k in keys1]
        values1 = hdoc.select('//b[contains(text(), "Insurance Carried")]//parent::div//table[@class="about-profile-details-table"]//thead//following-sibling::tr//td')
        values1 = [textify(v) for v in values1]
        insurance_carried = dict(zip(keys1, values1))
        item.set('insurance_carried', insurance_carried)

        things_about_service_provider = hdoc.select('//b[contains(text(), "Things You May Not Know About Me")]//parent::div//ul//li')
        things_about_service_provider = [textify(t) for t in things_about_service_provider]
        item.set('things_about_service_provider', things_about_service_provider)

        item.textify('green_certification', '//b[contains(text(), "Green Certifications")]//parent::div//ul//li')
        quick_facts = hdoc.select('//div[@class="about-profile-detail"]//ul[@class="checks"]//li')
        quick_facts = [textify(q) for q in quick_facts]
        item.set('quick_facts', quick_facts)

        image_url = hdoc.select('//div[@class="albumThumbnail"]/@style')
        image_url = [textify(i).replace('background: url(', '').replace(') no-repeat center top;', '') for i in image_url]
        item.set('image_url', image_url)

        community_involvement = textify(hdoc.select('//b[contains(text(), "Community Involvement")]//parent::div')).replace('Community Involvement', '').strip()
        item.set('community_involvement', community_involvement)

        average_rating = textify(hdoc.select('//div[@id="oss-composite"]'))
        item.set('average_rating', (average_rating))
        item.textify('reviews_count', '//a[@class="ratings-page-reset"]', lambda x: x.split(' Verified Ratings')[0])
        item.set('average_rating', average_rating)
        reviews_count = textify(hdoc.select('//a[@class="ratings-page-reset"]')).strip()
        reviews_count = reviews_count.split(' ')[0]
        if reviews_count:
            item.set('reviews_count', int(reviews_count))

        nodelist = hdoc.select('//div[@class="a-rating"]')
        reviews = []
        for node in nodelist:
            details = {}
            review_rating = textify(node.select('.//div[@class="rating-details-trigger smp_detailsCT"]//div/text()[contains(., ".")]'))
            details['review_rating'] = float(review_rating)
            details['review_date'] = textify(node.select('.//span[@class="dtreviewed"]'))
            details['reviewer'] = textify(node.select('.//span[@class="reviewer vcard"]//span[@class="fn"]'))
            details['reviewer_location'] = textify(node.select('.//span[@class="reviewer vcard"]//span[@class="locality"]')).replace('in ', '')
            details['review_project'] = textify(node.select('.//span[@class="summary"]')).replace('Project: ', '')
            details['review_description'] = textify(node.select('.//span[@class="description"]'))
            reviews.append(details)
        item.set('recent_reviews', reviews)

        yield item.process()
