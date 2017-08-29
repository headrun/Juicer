from juicer.utils import *
from datetime import datetime
def gen_start_urls():
    items = lookup_items('amazon_terminal', 'got_review_page:False', limit=100)
    for _id, term, data in items:
        yield data

def fill_review_details(item, review):
    date = textify(review.select('.//span[@style="vertical-align:middle;"]/nobr'))
    title = textify(review.select('.//span[@style="vertical-align:middle;"]/b'))
    member_name = textify(review.select('.//a[contains(@href,"/profile/")]/span/text()'))
    member_link = textify(review.select('.//a[contains(@href,"/profile/")]/@href'))
    reviews_from_member = textify(review.select('.//a[contains(@href,"/member-reviews/")]/@href'))
    review_text = textify(review.select('./text()'))
    permalink = textify(review.select('.//span[@class="tiny"]/a[contains(text(), "Permalink")]/@href'))
    rating = textify(review.select('.//span[contains(@title,"out of 5 stars")]/span/text()'))
    usefullness = textify(review.select('./div[contains(text(),"following review helpful")]/text()'))

    #refining certain data
    rating = float(rating.split()[0])
    date = date.replace(',', '')
    date = datetime.strptime(date, '%B %d %Y')
    #storing it in item
    item.set('date', date)
    item.set('title', title)
    item.set('member_name', member_name)
    item.set('member_reviews', reviews_from_member)
    item.set('member_link', member_link)
    item.set('text', review_text)
    item.set('review_rating', rating)
    item.set('usefullness', usefullness)

    #finding sk
    split_perm = permalink.split('/')
    sk = split_perm[split_perm.index('review') + 1]
    item.set('sk', sk)

class AmazonReviewSpider(JuicerSpider):
    name = 'amazon_reviews'
    start_urls = gen_start_urls()

    def parse(self, response):
        hdoc = HTML(response)
        #we know all urls we get point to Review pages
        url = response.url
        split_url = url.split('/')
        asin = split_url[split_url.index('product-reviews') + 1]
        if not asin:
            return
        reviews = hdoc.select('//table[@id="productReviews"]//div[@style="margin-left:0.5em;"]')
        for review in reviews:
            item = Item(response, HTML)
            fill_review_details(item, review)
            yield item.process()

        next_page = hdoc.select('//span[@class="paging"]/a/@href')
        if next_page:
            next_page = next_page[-1]
            yield Request(next_page, self.parse, response)
        else:
            item = Item(response, HTML)
            item.set('sk', asin)
            item.set('got_review_page', True)
            item.update_mode = 'custom'
            item.spider = 'amazon_terminal'
            yield item.process()

    @staticmethod
    def _update_item(new_data, old_data):
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

SPIDER = AmazonReviewSpider()
