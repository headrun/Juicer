from juicer.utils import *
from dateutil import parser

class RakutenJapanReviews(JuicerSpider):
    name = 'rakuten_jp_reviews'
    start_urls = 'http://review.rakuten.co.jp/item/1/203677_10374125/1.1/sort6/'

    def parse(self,response):
        hdoc = HTML(response)
        product_title = textify(hdoc.select('//h2[@class="revItemTtl fn"]//a/text()'))
        product_link = textify(hdoc.select('//h2[@class="revItemTtl fn"]//a/@href'))
        avg_rating = textify(hdoc.select('//span[@class="revEvaNumber average"]/text()'))
        nodes = hdoc.select('//div[@class="revRvwUserSec hreview"]')
        for node in nodes:
            date = textify(node.select('.//span[@class="revUserEntryDate dtreviewed"]/text()'))
            review_rating = textify(node.select('.//span[@class="revUserRvwerNum value"]/text()'))
            author_name = textify(node.select('.//dt[@class="revUserFaceName"]/span/text()'))or textify(node.select('.//dt[@class="revUserFaceName reviewer"]/a/text()'))
            author_url = textify(node.select('.//dt[@class="revUserFaceName"]/span/@href'))or textify(node.select('.//dt[@class="revUserFaceName reviewer"]/a/@href'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            text = textify(node.select(' .//dd[@class="revRvwUserEntryCmt description"]//text()'))
            title = textify(node.select('.//dt[@class="revRvwUserEntryTtl summary"]//text()'))
            comment_link = textify(node.select('.//dd[@class="revRvwUserEntryOther"]/a/@href'))
            sk = comment_link

            item = Item(response)
            item.set('url',xcode(comment_link))
            item.set('title',xcode(product_title) + '##<>##' +xcode(title))
            item.set('product_url',xcode(product_link))
            item.set('dt_added',dt_added)
            item.set('avg_rating',avg_rating)
            item.set('user_rating',review_rating)
            item.set('author',{'name':xcode(author_name),'url':author_url})
            item.set('text',xcode(text))
            item.set('sk',md5(sk))
            item.set('is_ecomm',True)
            item.set('xtags', ['japan_country_manual', 'reviews_sourcetype_manual', 'ecomm_reviews_sourcetype_manual'])
            yield item.process()

        nxt_pg = textify(hdoc.select('//div[@class="revPagination"]/a[last()]/@href'))
        yield Request(nxt_pg,self.parse,response)
