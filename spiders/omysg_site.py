from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urlparse import urljoin
from juicer.utils import *

class OmySite(JuicerSpider):
    name = "omysite"
    start_urls = "http://www.omy.sg/"
    allow_domian = ['http://showbiz.omy.sg/', 'http://lifestyle.omy.sg/', 'http://news.omy.sg/', 'http://yzone.omy.sg/', 'http://eat.omy.sg/']

    def parse(self, response):
        hdoc = HTML(response)

        self.latest_dt = parse_date('28/07/2013 11:33')
        nodes = hdoc.select('//ul[@id="nav"]/li//ul/li/a/@href').extract()
        for url in nodes:
            yield Request(url, self.parse_next, response)

    def parse_next(self,response):
        hdoc = HTML(response)
        table1 = hdoc.select('//detail/ul/li')
        nxt_page = ''
        for tab in table1:
            posted_dt = textify(tab.select('.//span[@class="stamp"]'))
            posted_dt = parse_date(posted_dt, True)
            if posted_dt >= self.latest_dt:
                self.update_dt(posted_dt)
                terminal_link = textify(tab.select('.//a[@class="title"]/@href'))
                if "blog.omy" in terminal_link:continue
                yield Request(terminal_link, self.parse_terminal, response)

        nxt_page = textify(hdoc.select('//li/a[contains(text(),"next")]/@href'))
        if nxt_page:
            yield Request(nxt_page, self.parse_next, response)


    def parse_terminal(self, response):
        hdoc = HTML(response)
        item = Item(response)
        title = textify(hdoc.select("//h1[@id='storytitle']/text()").extract())
        item.set('title', title)
        item.set('url', response.url)
        item.set('category', response.meta['title'])
        dt_added = textify(hdoc.select("//detail[@class='publication']//span[@class='stamp']/text()"))
        dt_added = get_timestamp(parse_date(dt_added, True)-datetime.timedelta(hours=8))
        item.set('dt_added', dt_added)
        author_url = textify(hdoc.select("//span[@class='contributor']/a/@href"))
        author = textify(hdoc.select("//span[@class='contributor']/a//text()").extract()).encode("utf-8")
        if author_url:
                item.textify('author.name', "//span[@class='contributor']/a//text()")
                author_url = urlparse.urljoin(response.url, author_url)
                item.set('author.url', author_url)
        text = textify(hdoc.select('//div[@class="story-view"]//text()').extract())
        item.set('text',text)
