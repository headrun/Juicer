from juicer.utils import *

class Flipkart(JuicerSpider):
    name = 'flipkart_reviews'
    start_urls = ['http://www.flipkart.com/']

    def parse(self, response):
        hdoc = HTML(response)

        if self.latest_dt:
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        categories = hdoc.select_urls(['//a[contains(@href,"header")]/@href'], response)

        for category in categories:
            if '/books?' in category:
                category = category.replace('/books?_pop=mheader','/books/pr?sid=bks&layout=grid')
            yield Request(category, self.parse_category, response)


    def parse_category(self, response):
        hdoc = HTML(response)

        sub_category = hdoc.select('//div[@class="line"]//div[not(contains(@id,"Kids-Categories"))]\
                                                  //ul//li[contains(@class,"listitem")]/parent::ul')

        if sub_category:
            for sub in sub_category:
                if sub.select('.//li[contains(@class,"listitem")]/a[contains(text(),"All")and\
                                                        not(contains(text(),"All-in-One"))]'):
                    link = textify(sub.select('.//li[contains(@class,"listitem")]/\
                                                            a[contains(text(),"All")]/@href'))
                    yield Request(link, self.parse_category, response)
                else:
                    urls = sub.select_urls(['.//li[contains(@class,"listitem")]/a/@href'], response)
                    for url in urls:
                        yield Request(url, self.parse_category, response)

        else:
            next_url = textify(hdoc.select('//div[@id="pagination"]//a[@class="next"]/@href'))
            terminals = hdoc.select_urls(['//div[@id="products"]//div[@class="title"]/a/@href|\
                                          //div[@id="products"]//a[@class="title"]/@href'], response)

            for terminal in terminals:
                yield Request(terminal, self.parse_subcat, response)
            (yield Request(next_url, self.parse_category, response)) if next_url else ''


    def parse_subcat(self, response):
        hdoc = HTML(response)

        review = textify(hdoc.select('//div[contains(@class,"section1")]//a[contains(text(),"Review")\
                                                      and contains(@href, "product-reviews")]/@href'))

        if review:
            yield Request(review, self.parse_subcat, response)
        if not review:
            nextpage_url = ''
            reviews = hdoc.select('//div[@class="review-list"]//div[contains(@class,"review line")]')
            for rev in reviews:
                date = parse_date(textify(rev.select('.//div[contains(@class,"date")]//text()')))
                if date >= self.latest_dt:
                    if self.flag:
                        self.update_dt(date)
                    nextpage_url = textify(hdoc.select('//div[contains(@class,"review")]//\
                                                        a[contains(text(),"Next")]/@href'))
                    url = rev.select('.//div[@class="unitExt"]//a[contains(text(),"Permalink")]/@href')
                    yield Request(url, self.parse_terminal, response)

            (yield Request(nextpage_url, self.parse_subcat, response)) if nextpage_url else ''


    def parse_terminal(self, response):
        hdoc= HTML(response)
        item = Item(response)

        # reviews
        date = parse_date(textify(hdoc.select('//div[contains(@class,"date")]//text()')))
        title = textify(hdoc.select('//div[contains(@class,"title")]//h2//a/text()'))
        title = title.encode('UTF-8').replace('&amp;','&')
        title = title.decode('ascii','ignore')
        price = textify(hdoc.select('//div[@class="line"]//div[contains(@class,"price")]\
                                          /span[contains(@class,"price")]//text()|//div\
                    [contains(text(),"Price")]/span[contains(@class,"price")]//text()'))
        price = (int(''.join(re.findall(r'\d+', price)))) if price else ''

        author = hdoc.select('//div[@class="line"]//a[contains(@href,"user")]/text()')
        if not author:
            author = hdoc.select('//div[@class="unit size1of5 section1"]//div[@class="line"]/span//text()')
        author = textify(author).encode('UTF-8').decode('ascii','ignore').replace('&amp;','&')

        a_url = hdoc.select('//div[@class="line"]//a[contains(@href,"user")]/@href')
        a_id = ''.join(re.findall(r'user-profiles/(.*)', textify(a_url)))
        rating = hdoc.select('//div[@class="line"]//div[contains(@class,"stars")]/@title')
        rating = (int(''.join(re.findall(r'\d+', textify(rating))))) if rating else ''
        text = hdoc.select('//div[contains(@class,"lastUnit")]//p[@class="line bmargin10"]//text()')
        text = textify(text).encode('UTF-8').replace('&amp;','&').replace('&gt;','>')

        item.set('dt_added', date)
        item.set('title', xcode(title))
        item.set('url', xcode(response.url))
        item.set('author.name', xcode(author))
        item.set('author.id', xcode(a_id)) if a_id else ''
        item.set('num.price', xcode(price)) if price else ''
        item.set('num.rating', xcode(rating)) if rating else ''
        item.set('author.url', xcode(textify(a_url))) if a_url else ''
        item.set('text', xcode(re.sub(r' +',' ', text.decode('ascii','ignore').replace('&lt;','<'))))

        yield item.process()

