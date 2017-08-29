from juicer.utils import *

class Zomato(JuicerSpider):
    name = 'zomato_shiro'
    start_urls = [
        'http://www.zomato.com/bangalore/shiro-lavelle-road/reviews',
        'http://www.zomato.com/mumbai/shiro-lower-parel/reviews',
        'http://www.zomato.com/ncr/shiro-hotel-samrat-chanakyapuri-delhi/reviews'
        ]

    def parse(self, response):
        hdoc = HTML(response)

        reviews = hdoc.select_urls(['//div[@class="zs-following-list"]/div[contains(@class,"res-review")]//a[@class="res-review-date"]/@href'], response)
        for review in reviews:
            yield Request(review, self.parse_terminal, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)
        item = Item(response)

        post_dt = textify(hdoc.select('//div[@class="res-review-top-right-text"]/a[@class="res-review-date"]'))
        post_dt = parse_date(post_dt)
        title = textify(hdoc.select('//h1[@class="heading1"]//text()'))
        author = textify(hdoc.select('//div[@class="user-snippet-name"]/a/text()'))
        a_url = textify(hdoc.select('//div[@class="user-snippet-name"]/a/@href'))
        a_reviews = textify(hdoc.select('//div[@class="user-snippet-stats"]/span[@class="user-snippet-stat"][1]'))
        a_followers = textify(hdoc.select('//div[@class="user-snippet-stats"]/span[@class="user-snippet-stat"][2]'))

        a_rating = textify(hdoc.select('//div[@class="res-review-top-right"]//div[contains(@class,"small-rating")]'))
        text = textify(hdoc.select('//div[@class="res-review-body clearfix"]/div/p'))
        text = re.sub(r' +', ' ', text)
        thanks = textify(hdoc.select('//div[@class="res-review-stat-box"]\
                  //span[@class="res-review-stat-count stats-thanks"]'))
        comments = textify(hdoc.select('//div[@class="res-review-stat-box"]\
                    //span[@class="res-review-stat-count stats-comment"]'))

        location = textify(hdoc.select('//div[@class="top-res-box-zone"]'))
        city = textify(hdoc.select('(//a[@class="home"]/parent::span/\
               following-sibling::span/a[@itemprop="url"])[1]/span/text()'))
        address = location+' '+city
        rating = textify(hdoc.select('//div[@class="top-res-box-details"]//div[contains(@class,"rating")]'))
        try:
            rating = float(rating)
        except:
            rating = ''
            pass

        xtags = ['india_country_manual', 'news_sourcetype_manual']
        item.set('dt_added', post_dt)
        item.set('title', title)
        item.set('author.name', author)
        item.set('author.url', a_url)
        item.set('author.num.reviews', int(a_reviews)) if a_reviews else 0
        item.set('author.num.followers', int(a_followers)) if a_followers else 0
        item.set('author.num.rating', float(a_rating)) if a_rating else 0
        item.set('num.thanks', int(thanks)) if thanks else 0
        item.set('num.comments', int(comments)) if comments else 0
        item.set('num.rating', rating) if rating else 0
        item.set('text', text)
        item.set('address', address)
        item.set('url', response.url)
        item.set('xtags', xtags)

        yield item.process()
