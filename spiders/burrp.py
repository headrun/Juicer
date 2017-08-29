from juicer.utils import *

class DelhiBurrp(JuicerSpider):
    name = 'burrp'
    start_urls = ['http://mumbai.burrp.com/review/list.html',
                  'http://bangalore.burrp.com/review/list.html',
                  'http://chennai.burrp.com/review/list.html',
                  'http://delhi.burrp.com/review/list.html',
                  'http://pune.burrp.com/review/list.html',
                  'http://hyderabad.burrp.com/review/list.html',
                  'http://ahmedabad.burrp.com/review/list.html',
                  'http://kolkata.burrp.com/review/list.html',
                  'http://goa.burrp.com/review/list.html',
                  'http://jaipur.burrp.com/review/list.html',
                  'http://chandigarh.burrp.com/review/list.html',
                  'http://kochi.burrp.com/review/list.html']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.cutoff_dt = None
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.flag = False

    def parse(self, response):
        hdoc = HTML(response)


        if self.latest_dt:
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))
        twoweek_diff = datetime.timedelta(days=14)
        self.cutoff_dt = self.latest_dt - twoweek_diff

        next_page = ''
        reviews = hdoc.select("//li[@class='estab_reviewtext']")

        for review in reviews:
            date = textify(review.select("(./h3/span[contains(@class,'revDate')]/text())"))
            if 'min' in date:date = re.sub('min', 'minute', date)
            if 'secs' in date:date = ''
            posted_date = parse_date(date)
            if posted_date >= self.cutoff_dt:
                url = textify(review.select("(./h4/a[contains(@href,'UR__reviews')]/@href)"))
                next_page = "".join(textify(hdoc.select("//ul[@class='pagination inline']/li\
                                                        /a[contains(text(),'Next')]/@href")))
                yield Request(url, self.parse_reviews, response)

        if next_page:
            yield Request(next_page, self.parse, response)

    def parse_reviews(self, response):
        hdoc = HTML(response)

        next_page = ''
        reviews = hdoc.select("//div[contains(@class,'listShadow')]/ul[contains(@class,'estab_review')]")
        for review in reviews:
            post_dt = textify(review.select("(./li/h3/span[contains(@class,'revDate')]/text())"))
            if 'min' in post_dt:post_dt = re.sub('min', 'minute', post_dt)
            if 'secs' in post_dt:post_dt = ''
            if parse_date(post_dt) >= self.latest_dt:
                url = textify(review.select(".//a[@class='url']/@href"))
                next_page = hdoc.select("//ul[@class='pagination inline']/li\
                                            /a[contains(text(),'Next')]/@href")
                next_page = textify(next_page)
                yield Request(url, self.parse_terminal, response)

        if next_page:
            yield Request(next_page, self.parse_reviews, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        data = hdoc.select("//div[contains(@class,'hReview-aggregate')]")
        review = data.select(".//ul[contains(@class,'estab_review')]")
        item = Item(response)

        post_date = textify(review.select(".//span[contains(@class,'revDate')]/text()"))
        if 'min' in post_date:post_date = re.sub('min', 'minute', post_date)
        if 'secs' in post_date:post_date = ''
        posted_date = parse_date(post_date)
        if posted_date >= self.latest_dt:
            author = {}
            if self.flag:
                self.update_dt(posted_date)
            title = re.sub('Reviews of ','',textify(data.select(".//div[@class='estab']/h3/a/text()"))\
                            .replace('&amp;','&').encode('UTF-8'))
            item.set('title', xcode(title.decode('ascii', 'ignore')))
            text = textify(review.select(".//div[contains(@id,'review_')]//text()"))\
                                            .replace("\'","'").replace("&amp;",'&')\
                                            .replace("&gt;",'>').replace("&lt;",'<')\
                                            .replace("\t",'').replace('\n','').encode("UTF-8")
            item.set('dt_added', posted_date)
            item.set('text', re.sub(r' +',' ', xcode(text.decode('ascii', 'ignore'))))
            url = textify(review.select(".//a[@class='url']/@href"))
            item.set('url', xcode(url))
            author_name = textify(review.select(".//span[@class='reviewer']//text()")).replace('&amp;','&')
            if author_name:
                item.set('author.name', xcode(author_name))
            author_url = textify(review.select(".//a[@class='reviewbyUserID']/@href"))
            if author_url:
                item.set('author.url', xcode(author_url))
                author_id =  "".join(re.findall("user/\w+_(\d{11})", author_url))
                if author_id:
                    item.set("author.id", xcode(author_id))
            category = data.select(".//li[contains(@class,'new_Icon')]//h2/a")
            category = [xcode(textify(cat.select("./text()")).replace('&amp;','&')) for cat in category if cat.select("./text()")]
            item.set('category', category) if category else ''
            rating = textify(review.select(".//span[@class='rating']/span/@title"))
            if rating:
                author['rating'] = xcode(int(rating))
                item.set('num', author)
            street_address = textify(data.select('.//span[@class="street-address"]/text()'))
            street_address = street_address.encode('utf8').decode('ascii','ignore').replace('&amp;','&')
            locality = textify(data.select('.//span/a[@class="locality"]/text()'))
            locality = locality.encode('utf8').decode('ascii','ignore').replace('&amp;','&')
            region = textify(data.select('.//span[@class="region"]/text()'))
            region = region.encode('utf8').decode('ascii','ignore').replace('&amp;','&')
            item.set('street_address', xcode(street_address)) if street_address else ''
            item.set('locality', xcode(locality)) if locality else ''
            item.set('region', xcode(region)) if region else ''
            ob = pprint.PrettyPrinter(indent=2)
            #ob.pprint(item.data)
