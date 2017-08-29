from juicer.utils import *
from dateutil import parser

class AmazonJapanreviews(JuicerSpider):
    name = 'amazon_jp_reviews'
    start_urls = 'http://www.amazon.co.jp/product-reviews/B00KHNZQKE/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=1'

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="cm_cr-review_list"]/div[@class="a-section review"]')
        product_title = textify(hdoc.select('//div[@class="a-row product-title"]//a/text()'))
        product_link = textify(hdoc.select('//div[@class="a-row product-title"]//a/@href'))
        if 'http' not in product_link: product_link = 'http://www.amazon.co.jp' + product_link

        for node in nodes:
            _id = textify(node.select('.//@id[1]'))
            author = textify(node.select('.//span[contains(@class,"review-byline")]/a/text()')) or textify(node.select('.//span[contains(@class,"review-byline")]/text()'))
            author_link =textify(node.select('.//span[contains(@class,"review-byline")]/a/@href'))
            if 'http' not in author_link:author_link = 'http://www.amazon.co.jp' + author_link
            date = textify(node.select('.//span[contains(@class,"review-date")]'))
            date = '/'.join(re.findall('\d+',date))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            title = textify(node.select('.//a[contains(@class,"review-title")]/text()'))
            title_link = textify(node.select('.//a[contains(@class,"review-title")]/@href'))
            if 'http' not in title_link: title_link = 'http://www.amazon.co.jp' + title_link
            text = textify(node.select('.//span[contains(@class,"review-text")]//text()'))
            rating = textify(node.select('.//i[contains(@class,"review-rating")]/span/text()'))
            if rating: rating = rating.split(u'\u3064\u661f\u306e\u3046\u3061')[-1]
            url = response.url + '#' + _id
            sk = hashlib.md5(url).hexdigest()

            item = Item(response)
            item.set('url',response.url + '#' + _id)
            item.set('title',xcode(title + '##<>##' + product_title))
            item.set('product_url',xcode(product_link))
            item.set('dt_added',dt_added)
            item.set('author',xcode(author))
            item.set('author',{'name':xcode(author),'url':author_link})
            item.set('rating',rating)
            item.set('text',xcode(text))
            item.set('is_ecomm',True)
            item.set('xtags', ['japan_country_manual', 'reviews_sourcetype_manual', 'ecomm_reviews_sourcetype_manual'])
            yield item.process()

        next_pg = textify(hdoc.select('//li[@class="a-last"]/a/@href'))
        if next_pg:
           next_pg = 'http://www.amazon.co.jp' +  xcode(next_pg)
           yield Request(next_pg,self.parse,response)
