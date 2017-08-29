from juicer.utils import *
from dateutil import parser

class JebanReviews(JuicerSpider):
    name = 'jeban_reviews'
    start_urls = ['http://jeban.com/reviews_list.php']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False

    def parse(self,response):
        hdoc = HTML(response)

        if self.latest_dt is None :
            self.latest_dt = self._latest_dt
            self.flag = True

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=7)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select('//div[@class="product-detail"]/parent::a/@href').extract()

        for node in nodes:
            if 'http' not in node: node = 'http://jeban.com/' + node
            yield Request(node,self.parse_next,response)

        next_page = textify(hdoc.select('//div[@class="panel-footer clearfix"]//a[@class="btn btn-default btn-sm"]/@href'))
        if next_page:
            next_page = 'http://jeban.com/reviews_list.php' + next_page
            yield Request(next_page,self.parse,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        reviews_link = textify(hdoc.select('//a[@class="btn btn-primary"]/@href'))
        if 'http' not in reviews_link: reviews_link = 'http://jeban.com/reviews_product.php' + reviews_link
        yield Request(reviews_link,self.review_details,response)

    def review_details(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//div[@class="page-header"]/h1/text()'))
        brand = textify(hdoc.select('//h2[@class="brand-name"]/text()')[0])
        product = textify(hdoc.select('//h3[@class="product-name"]/text()')[0])
        category = textify(hdoc.select('//dl[@class="dl-horizontal"]//ul/li/a/text()')).replace(' ',',')
        threads = hdoc.select('//div[contains(@class,"panel panel-default review")]')

        for thread in threads:
            review_id = textify(thread.select('.//@data-review-id'))
            author_name = textify(thread.select('.//div[@class="pull-left clearfix hidden-xs"]//a/strong/text()'))
            author_url = textify(thread.select('.//div[@class="pull-left clearfix hidden-xs"]//a/@href'))
            if 'http' not in author_url: author_url = 'http://jeban.com/' + author_url
            age = textify(thread.select('.//ul[@class="list-unstyled"]/li//text()').extract()[0])
            other_info = thread.select('.//ul[@class="list-unstyled"]/li//text()').extract()[1:]
            date = textify(thread.select('.//i[@class="fa fa-clock-o"]/parent::li/@title'))
            date = parse_date(xcode(date))
            dt_added = get_timestamp(date - datetime.timedelta(hours=7))

            if date < self.cutoff_dt:
                is_next = False
                continue
            rating = textify(thread.select('.//span[@class="label label-default"]/text()'))
            text = textify(thread.select('.//p[@class="review-detail clearfix"]/text()'))
            individual_ratingcategory = thread.select('.//table[@class="pull-right hidden-xs"]/tbody//td[@data-rating]/preceding-sibling::td/text()').extract()
            individual_ratings = thread.select('.//table[@class="pull-right hidden-xs"]/tbody//td[@data-rating]/p/@title').extract()
            satisfaction = textify(thread.select('.//tr//td[@class="product-average-rating"]/preceding-sibling::td/text()'))
            satisfaction_rating = textify(thread.select('.//tr//td[@class="product-average-rating"]/p/@title'))
            sk = review_id + str(date) + author_name

            '''item = Item(response)
            item.set('url',xcode(response.url))
            item.set('title',xcode(title))
            item.set('brand',xcode(brand))
            item.set('product',xcode(product))
            item.set('category',xcode(category))
            item.set('review_id',review_id)
            item.set('author',{'name':xcode(author_name),'url':author_url,'age':age,'other_info':xcode(other_info)})
            item.set('dt_added',dt_added)
            item.set('rating',rating)
            item.set('sk',md5(sk))
            item.set('text',xcode(text))

            for x in xrange(len(individual_ratingcategory)):
                item.set('all_rating',textify(xcode(individual_ratingcategory[x] + ':' + individual_ratings[x])))
            item.set('satisfaction_rating', xcode(satisfaction) + ':' + satisfaction_rating)'''

            print '\n'
            print response.url
            print self.cutoff_dt
            print 'title',xcode(title)
            print 'brand',xcode(brand)
            print 'product',xcode(product)
            print 'category',xcode(category)
            print 'dt_added',dt_added
            print 'text',xcode(text)
            print 'author',xcode(author_name)

        try:nxt_page = hdoc.select('//a[@class="btn btn-default btn-sm"]/@href').extract()[0]
        except:nxt_page= ''
        if nxt_page != '' and is_next:
            nxt_page = 'http://jeban.com/reviews_product.php' + nxt_page
            yield Request(nxt_page,self.review_details,response)
