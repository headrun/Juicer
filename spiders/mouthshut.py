from juicer.utils import *

class MouthShut(JuicerSpider):
    name  = "mouthshut"
    start_urls = ['http://www.mouthshut.com/product/products.php']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
            self.flag = False

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select_urls(['//div[@id="middle"]//table//li//a/@href'], response)

        if self.latest_dt is None:
            self.latest_dt = self._latest.dt
            self.flag = True

        for url in urls:
            yield Request(url, self.parse_next, response)

    def parse_next(self, response):
        hdoc = HTML(response)
        urls = hdoc.select_urls(['//a/@href'], response)

        for url in urls:
            if "reviews" in url:
                yield Request(url, self.parse_reviews, response)
            elif "categories" in url:
                yield Request(url, self.parse_next, response)

    def parse_reviews(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="allreviews"]//div[@class="hreview"]')
        title = textify(hdoc.select('//div[@class="heading_green1"]//h2/text()'))
        rating = hdoc.select('//span[@class="prorating_full"]')
        rating = len(rating)
        tag = []
        tag.append(title)

        for node in nodes:
            author = {}
            num = {}
            dt_added = textify(node.select('.//span[@class="datetime"]//span[@class="dtreviewed"]//span[@class="value-title"]/text()'))
            dt_added = parse_date(dt_added)

            if dt_added and dt_added > self.latest_dt:

                review_title = textify(node.select('.//span[@class="reviewtitle"]'))
                url = textify(node.select('.//span[@class="reviewtitle"]//h2//a/@href'))
                reviewer_name = textify(node.select('.//span[@class="reviewer"]//text()'))
                reviewer_url = textify(node.select('.//li[@class="profile"]//div//a[contains(@id,"lnkuser")]/@href'))#.split(" ")[0]
                location = textify(node.select('.//li[@class="profile"]//span[@class="smallfontgrey"]//text()'))
                categ = textify(hdoc.select('//div[@class="hierarchy"]//a[2]'))
                review = textify(hdoc.select('.//span[@class="rev-count1 fl"]//h2//text()'))
                author_review = textify(node.select('.//li[@class="profile"]//div//a[contains(@id,"_revlink")]//text()'))
                author_review = re.findall(r'\d+', author_review)
                review =  re.findall(r'\d+', review)
                author_blog = textify(node.select('.//li[@class="profile"]//div//a[contains(@id,"_diarylink")]//text()'))
                author_blog = re.findall(r'\d+', author_blog)
                if review:
                    num["reviews"] = int(review[0])

                num['rating'] = rating
                review_title = textify(node.select('.//span[@class="reviewtitle"]//h2//a/text()'))
                author["name"] = reviewer_name
                author["url"] = reviewer_url
                author["location"] = location
                if author_review:
                    author['review'] = int(author_review[0])

                if author_blog:
                    author['blog'] = int(author_blog[0])

                read_more_url = textify(node.select('.//span//a//@href[contains(string(), "mouthshut")]')).split(" ")
                read_more_url = read_more_url[0]

                if read_more_url:
                    yield Request(read_more_url , self.parse_article, response, meta = {'review_title': review_title, 'dt_added': dt_added, 'author':author, 'num':num, 'title':title, 'tag':tag,'category':categ, 'url':url})
                else:
                    item = Item(response)
                    item.set("title", tag)
                    item.set("category", categ)
                    item.set('title', review_title)
                    item.set('url', url)
                    item.set("dt_added", dt_added)
                    item.set("author", author)
                    item.set("num", num)
                    item.set('title', review_title)

                    review = textify(node.select('.//span[@class="summary"]//p/text()'))
                    item.set("text", review)
                    yield item.process()

    def parse_article(self, response):
        hdoc = HTML(response)

        item = Item(response)
        item.set('title', response.meta['review_title'])
        item.set('dt_added', response.meta['dt_added'])
        item.set("author", response.meta['author'])
        item.set('tag', response.meta['tag'])
        item.set('num', response.meta['num'])
        item.set('category', response.meta['category'])
        text = textify(hdoc.select("//span[@class='description']//p/text()"))
        item.set('text', text)
        item.set('url', response.meta['url'])
        yield item.process()
