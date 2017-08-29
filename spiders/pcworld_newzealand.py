from juicer.utils import *
from dateutil import parser

class Pcworldnewzealand(JuicerSpider):
    name = 'pcworld_newzealand'
    start_urls = ['http://www.pcworld.co.nz/section/mobile_phones/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//nav[@id="section_nav"]//li/a/@href').extract()

        for node in nodes:
            if 'http' not in node: node = 'http://www.pcworld.co.nz' + node
            yield Request(node,self.articles,response)

    def articles(self,response):
        hdoc = HTML(response)
        threads = hdoc.select('//article[@class="summary news"]/a/@href').extract() or hdoc.select('//h3[@class="review-list-name"]/a/@href').extract()

        for thread in threads:
            #if 'http' not in thread: thread = 'http://www.pcworld.co.nz'  + thread
            thread = 'http://www.pcworld.co.nz/review/sony/xperia_m/526662/'
            yield Request(thread,self.details,response)

        nxt_pg = textify(hdoc.select('(//li[@class="next"])[last()]/a/@href'))
        if nxt_pg:
            nxt_pg = 'http://www.pcworld.co.nz' + nxt_pg
            yield Request(nxt_pg,self.articles,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="name"]/text()'))
        art_sms = textify(hdoc.select('//p[@class="art-sms"]/text()')) or textify(hdoc.select('//h2/span[@itemprop="description"]/text()'))
        author_name = textify(hdoc.select('//span[@itemprop="author"]/text()')) or textify(hdoc.select('//p[@class="author"]/a/text()'))
        author_link = textify(hdoc.select('//p[@class="art-byline"]/a/@href')) or textify(hdoc.select('//p[@class="author"]/a/@href'))
        if 'http' not in author_link: author_link = 'http://www.pcworld.co.nz' + author_link
        date = textify(hdoc.select('//span[@itemprop="datePublished"]/text()')) or textify(hdoc.select('//p[@itemprop="datePublished"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=13))
        text = textify(hdoc.select('//div[@class="art-body"]/p//text() | //div[@class="art-body"]/h3/text() ')) or textify(hdoc.select('//div[@class="review_body_text"]/p//text()'))
        text = textify(text.strip('Join the PC World New Zealand newsletter!'))
        rating = textify(hdoc.select('//span[@itemprop="ratingValue"]/text()'))
        pros = textify(hdoc.select('//div[@class="snapshot-pros"]/ul//li//text()'))
        cons = textify(hdoc.select('//div[@class="snapshot-cons"]/ul//li//text()'))

        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'art_sms',xcode(art_sms)
        print 'author',{'name':author_name,'url':author_link}
        print 'date',dt_added
        print 'text',xcode(text)
        print 'rating',rating
        print 'pros',xcode(pros)
        print 'cons',xcode(cons)

        user_reviews = textify(hdoc.select('//li/a[@class="user-review-tab"]/@href'))
        if user_reviews: user_reviews = 'http://www.pcworld.co.nz' + user_reviews
        import pdb;pdb.set_trace()
        yield Request(user_reviews,self.user_comments,response)

    def user_comments(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        product_title = textify(hdoc.select('//h1[@class="review_product_name"]/text()'))
        product_description = textify(hdoc.select('//span[@itemprop="description"]/text()'))
        comments = hdoc.select('//div[@class="post-content"]//div[@class="post-body"]')

        for comment in comments:
            author_names = textify(commment.select('.//span[@class="author"]/text()'))
            comment_date = textify(comment.select('.//span/a[@data-role="relative-time"]/@title'))
            date_added = get_timestamp(parse_date(xcode(comment_date)) - datetime.timedelta(hours=13))
            comment_text = textify(comment.select('.//div[@data-role="message"]//p//text()'))

            print '\n'
            print response.url
            print 'tilte',xcode(product_title)
            print 'description',xcode(product_description)
            print 'auhtor',{'author.name':author_name}
            print 'date',comment_date
            print 'text',xcode(comment_text)
