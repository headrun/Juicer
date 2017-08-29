from juicer.utils import *

class MouthShutRecent(JuicerSpider):
    name = "mouthshutrecent"
    start_urls = "http://www.mouthshut.com/review/old-recent-reviews.php"

    def parse(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="producthelp1"]//table/tr//td[@valign="top"]')
        nextpage_url = textify(hdoc.select('//a[@class="Next"]/@href'))

        for node in nodes:
            link = textify(node.select('.//a/@href'))
            yield Request(link, self.parse_page, response)

        if nextpage_url:
            yield Request(nextpage_url, self.parse, response)

    def parse_page(self, response):
        hdoc = HTML(response)

        item = Item(response)
        author = {}
        title = textify(hdoc.select('//ul[@class="product-title"]//li//h1//span[@class="item"]//span//text()'))
        item.set('title', title)
        author_name = textify(hdoc.select('//span[@class="reviewer"]'))
        author_url = textify(hdoc.select('//span[@class="smallfontgrey"]//a/@href[contains(string(), "timeline")]'))
        author['name'] = author_name
        author['url'] = urlparse.urljoin(response.url, author_url)
        item.set('author', author)
        dt_added = textify(hdoc.select('//span[@class="dtreviewed"]//span/@title'))
        dt_added = parse_date(dt_added)
        item.set('dt_added', dt_added)
        text = textify(hdoc.select('//span[@class="description"]//p'))
        item.set('text', text)
        item.set('url', response.url)
        yield item.process()
