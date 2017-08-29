from juicer.utils import *

class Stockhouse(JuicerSpider):
    name = 'stockhouse'
    start_urls = ['http://www.stockhouse.com/news/natural-resources',
                  'http://www.stockhouse.com/news/business-news',
                  'http://www.stockhouse.com/news/micro-cap-report',
                  'http://www.stockhouse.com/news/canadian-press-releases',
                  'http://www.stockhouse.com/news/us-press-releases'
            ]

    def parse(self, response):
        hdoc = HTML(response)

        if self.latest_dt:
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        next_page = ''
        nodes = hdoc.select('//ul[@class="article-list"]/li')
        nodes = hdoc.select('//div[contains(@class, "article-container")]') if not nodes else nodes
        nodes = hdoc.select('//div[@class="press-releases-content"]//tr[@class="pr-row"]') if not nodes else nodes
        for node in nodes:
            post_dt = textify(node.select('./span[@class="story-date"]/text()'))
            post_dt = textify(node.select('.//td[@class="pr-date"]/text()')) if not post_dt else post_dt
            post_dt = textify(node.select('./div[@class="hub-source-date"]//text()')) if not post_dt else post_dt
            post_dt = post_dt.split('|')[-1].strip()
            post_dt = parse_date(post_dt)
            if post_dt >= self.latest_dt:
                if self.flag: self.update_dt(post_dt)
                url = textify(node.select('.//h3//a/@href'))
                url = textify(node.select('./td[@class="pr-headline"]/a/@href')) if not url else url
                title = textify(node.select('.//h3//a/text()'))
                title = textify(node.select('./td[@class="pr-headline"]/a/text()')) if not title else title
                next_page = textify(hdoc.select('//a[contains(text(),"Next")]/@href'))
                yield Request(url, self.parse_terminal, response, meta = {'post_dt' : post_dt, 'title' : title})
        if next_page:yield Request(next_page, self.parse, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)
        item = Item(response)

        title = response.meta['title']
        title = title.replace('\n','').replace('\t','').replace('&amp;','&')
        post_dt = response.meta['post_dt']
        text = textify(hdoc.select('//div[@class="news-article"]/div[contains(@class,"content")]'))
        text = textify(hdoc.select('//div[@class="content"]/div[@id="story"]')) if not text else text
        text = text.encode('utf8').replace('ascii','ignore')
        text = re.sub(r' +',' ', text.replace('\n','').replace('\t','').replace('&amp;','&')).replace('\r','')

        author = textify(hdoc.select('//td[@class="news-columnist-info-cell"]/a/text()'))
        author = textify(hdoc.select('//div[@class="heading"]//a/text()')) if not author else author
        author_url = textify(hdoc.select('//td[@class="news-columnist-info-cell"]/a/@href'))
        author_url = textify(hdoc.select('//div[@class="heading"]//a/@href')) if not author_url else author_url
        if author_url and not author_url.startswith('http'):
            author_url = urlparse.urljoin(response.url, author_url)
        tag = hdoc.select('//span[@class="big-tags"]/a')
        tags = [textify(i.select('./text()')) for i in tag if i]
        import pdb;pdb.set_trace()
"""
item.set('url', xcode(response.url))
        item.set('title', xcode(title))
        item.set('dt_added', xcode(post_dt))
        item.set('text', xcode(text))
        item.set('author.name', xcode(author))
        item.set('author.url', author_url) if author_url else ""
        item.set('tags', tags) if tags else ""

#        yield item.process()"""
