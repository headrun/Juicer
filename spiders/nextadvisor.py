from juicer.utils import *
class Honda(JuicerSpider):
    name = "nextadvisor"
    start_urls = ["http://www.nextadvisor.com/credit_cards/articles/19/best-travel-reward-credit-cards-analysis"]


    def parse_test(self,response):
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

    def parse(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="content_top"]/h1'))
        text = textify(hdoc.select('//div[@class="content_top"]//p'))
        text1 = textify(hdoc.select('//div[@class="wrap_result"]//text()'))
        text = text + text1
        date = textify(hdoc.select('//div[@class="content_top"]//p/strong'))
        text = text.replace(date, '')
        date = get_timestamp(parse_date(date) + datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', title)
        item.set('text', text.strip())
        item.set('url', response.url)
        item.set('dt_added', date)
        item.set('xtags', ['usa_country_manual', 'capitalone_project_manual', 'news_sourcetype_manual'])

        yield item.process()

