from juicer.utils import *
from dateutil import parser

class Yelp(JuicerSpider):
    name = 'yelp'
    start_urls = ['http://www.yelp.com/locations']

    def parse(self,response):
        hdoc = HTML(response)
        cities = hdoc.select('//div[@class="column column-alpha "]//ul[@class="cities"]//a/@href').extract()

        for city in cities[:2]:
            if 'http' not in city: city = 'http://www.yelp.com' + city
            yield Request(city,self.parse_category,response)

    def parse_category(self,response):
        hdoc = HTML(response)
        categories_tab = hdoc.select('//div[@class="navigation"]//li[@data-tab-id]/a/@href').extract()

        for category_tab in categories_tab[:3]:
            if 'http' not in category_tab: category_tab = 'http://www.yelp.com' + category_tab
            yield Request(category_tab,self.sub_category,response)

    def sub_category(self,response):
        hdoc = HTML(response)
        category_url = hdoc.select('//li[@class="clearfix"]//ul[@class="column-set"]//a/@href').extract()
        for category in category_url[:1]:
            if 'http' not in category: category = 'http://www.yelp.com/search?cflt=halal&find_loc=Atlanta%2C+GA&start=10#find_desc&start=0'
            yield Request(category,self.brands,response)

    def brands(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="search-results-content"]//div[@class="media-story"]//span[@class="indexed-biz-name"]/a/@href').extract()
        for node in nodes:
            if 'http' not in node: node = 'http://www.yelp.com/biz/falafel-cafe-marietta'
            yield Request(node,self.review_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="pagination-block"]//a[@class="page-option available-number"]/@href'))
        if nxt_pg and 'http' not in nxt_pg: nxt_pg = 'http://www.yelp.com' + nxt_pg
        yield Request(nxt_pg,self.brands,response)

        search_moreurl = textify(hdoc.select('//div[@id="best-of-category"]/a/@href'))
        if 'http' not in search_moreurl: search_moreurl = 'http://www.yelp.com/' + search_moreurl
        yield Request(search_moreurl,self.brands,response)

    def review_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        threads = hdoc.select('//div[@class="review-list"]//div[@class="review review--with-sidebar"]')

        for thread in threads:
            date = textify(thread.select('.//span[@class="rating-qualifier"]/meta/@content')) or textify(thread.select('.//div[@class="previous-review clearfix"]//span[@class="rating-qualifier"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=-5))
            if dt_added <  get_current_timestamp()-86400*200:
                continue
            if date != '':
                review_id = textify(thread.select('.//@data-review-id')[0])
                review_url = response.url + '?hrid=' + review_id
                user_name = textify(thread.select('.//li[@class="user-name"]/a/text()'))
                user_url =  textify(thread.select('.//li[@class="user-name"]/a/@href'))
                user_location = textify(thread.select('.//li[@class="user-location"]//text()'))
                text = textify(thread.select('.//p[@itemprop="description"]/text()')) or textify(thread.select('.//span[@class="js-content-toggleable hidden"]//text()'))


                print '\n'
                print response.url
                print review_id
                print xcode(user_name)
                print xcode(user_location)
                print date
                print dt_added
                print xcode(text)
                print review_url
