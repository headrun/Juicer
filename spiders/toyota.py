from juicer.utils import*
class Toyota(JuicerSpider):
    name = "toyota"
    start_urls = "http://www.toyotacarsindia.in/"

    def parse(self, response):
        hdoc=HTML(response)
        urls = hdoc.select_urls('//li[contains(@class, "cat-item")]/a/@href', response)

        #if self.latest_dt:self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        #else:self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))
        self.latest_dt = parse_date('2014-04-12')

        check_date = self._latest_dt + datetime.timedelta(hours=8)
        oneweek_diff = datetime.timedelta(days=7)
        self.cutoff_dt = check_date - oneweek_diff

        for url in urls:
            yield Request(url, self.parse_page, response)

    def parse_page(self,response):
        hdoc=HTML(response)
        nodes = hdoc.select('//div[@class="post-list"]//div[contains(@id, "post")]')
        for node in nodes:
            post_time = textify(node.select('.//span[@class="date"]'))
            post_time = parse_date(post_time)
            if post_time >= self.latest_dt:
                url =  textify(node.select('./a/@href'))
                yield Request(url,self.parse_next,response)
        next_url = textify(hdoc.select('//div[@id="content"]//div[@class="pagination"]//span[@class="left"]//a[contains(text()," Previous Entries")]/@href'))
        if next_url:
            yield Request(next_url,self.parse_page,response)

    def parse_next(self,response):
        hdoc=HTML(response)
        tags=[]
        title = textify(hdoc.select('//div[@id]//h1[@class="post-title"]'))
        tagsinfo=textify(hdoc.select('//span[@class="cat"]'))
        text = textify(hdoc.select('//div[@class="entry-content"]/p'))
        author = textify(hdoc.select('//div[@class="author_info"]/p//a[@rel="nofollow"]'))
        date = textify(hdoc.select('//span[@class="date"]'))
        date = parse_date(date) - datetime.timedelta(hours=1, minutes=30)
        tags = tagsinfo.split(",")

        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('author.name', author)
        item.set('dt_added', date)
        item.set('tags', tags)
        item.set('url', response.url)

        yield item.process()
