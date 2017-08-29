from juicer.utils import *
class Honda(JuicerSpider):
    name = "honda"
    start_urls = ["http://www.bangkokpost.com/news/politics", "http://www.bangkokpost.com/news/social", "http://www.bangkokpost.com/news/crime", "http://www.bangkokpost.com/news/security", "http://www.bangkokpost.com/news/sports", "http://www.bangkokpost.com/news/transport", "http://www.bangkokpost.com/news/asean", "http://www.bangkokpost.com/news/asia", "http://www.bangkokpost.com/news/world", "http://www.bangkokpost.com/news/special-reports", "http://www.bangkokpost.com/business/news", "http://www.bangkokpost.com/business/tourism-and-transport", "http://www.bangkokpost.com/business/telecom", "http://www.bangkokpost.com/business/finance", "http://www.bangkokpost.com/business/market-analysis", "http://www.bangkokpost.com/business/company-in-thailand", "http://www.bangkokpost.com/business/trade-and-conferences", "http://www.bangkokpost.com/opinion/opinion", "http://www.bangkokpost.com/learning/learning-from-news", "http://www.bangkokpost.com/learning/easy", "http://www.bangkokpost.com/learning/really-easy", "http://www.bangkokpost.com/learning/work", "http://www.bangkokpost.com/learning/learning-together", "http://www.bangkokpost.com/learning/news", "http://www.bangkokpost.com/tech/world-updates", "http://www.bangkokpost.com/tech/local-news", "http://www.bangkokpost.com/lifestyle/art-and-culture/music", "http://www.bangkokpost.com/lifestyle/art-and-culture/film", "http://www.bangkokpost.com/lifestyle/art-and-culture/book", "http://www.bangkokpost.com/lifestyle/art-and-culture/art", "http://www.bangkokpost.com/lifestyle/art-and-culture/nostalgia", "http://www.bangkokpost.com/lifestyle/family-and-health", "http://www.bangkokpost.com/lifestyle/food-and-drinks", "http://www.bangkokpost.com/lifestyle/social-and-lifestyle", "http://www.bangkokpost.com/lifestyle/news-and-pr", "http://www.bangkokpost.com/lifestyle/review", "http://www.bangkokpost.com/lifestyle/review", "http://www.bangkokpost.com/auto/news", "http://www.bangkokpost.com/auto/review", "http://www.bangkokpost.com/property/technique", "http://www.bangkokpost.com/property/news"]


    def parse(self,response):
        hdoc = HTML(response)

        #if self.latest_dt:self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        #else:self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))
        self.latest_dt = parse_date('2014-09-01')

        check_date = self._latest_dt + datetime.timedelta(hours=8)
        oneweek_diff = datetime.timedelta(days=7)
        self.cutoff_dt = check_date - oneweek_diff

        is_next = True
        nodes = hdoc.select('//div[@id="subChanelReview"]//li')
        for node in nodes:
            post_time = textify(node.select('./p/span[@class="date"]'))
            post_time = parse_date(post_time)

            if post_time >= self.latest_dt:
                url = node.select('./h3/a/@href')
                yield Request(url,self.parse_next,response)
            else:
                is_next = False
        next_url = textify(hdoc.select('//div[@class="subChanelDetail"]//p[@class="pageNavigation"]//a[contains(text(), "Next")]/@href'))
        if is_next and next_url:
            yield Request(next_url, self.parse, response)

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="headergroup"]//h2'))
        text = textify(hdoc.select('//div[@class="articleContents"]/p'))
        date = textify(hdoc.select('//span[@itemprop="datePublished"]'))
        author = textify(hdoc.select('//li[@itemprop="editor"]'))
        section = textify(hdoc.select('//div[@id="headergroup"]//li/a[@href="/search/news-and-article?xNewsSection=Business&xAdvanceSearch=true"]'))
        (m,n)=author.split(":")
        count = textify(hdoc.select('//div[@id="headergroup"]//ul/li//a[@href="javascript:void(0);"]'))
        view_count=textify(hdoc.select('//div[@id="headergroup"]//ul/li'))
        views = {}

        (dt,views,comments_count) = view_count.split("|")
        views = views.split(':')
        num = {}
        if len(views) ==2:
            num['views'] = int(views[1].replace(',', ''))
        num['comments'] = int(count.replace(',', ''))
        date = get_timestamp(parse_date(date.replace('.', ':')) - datetime.timedelta(hours=7))

        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('url', response.url)
        item.set('author.name', n.strip())
        item.set('dt_added', date)
        item.set('num', num)

        if date > 1396594385:
            yield item.process()

