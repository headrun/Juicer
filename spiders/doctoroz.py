from juicer.utils import *

class Doctoroz(JuicerSpider):
    name = 'doctoroz'
    start_urls = ['http://www.doctoroz.com/episodes']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False

    def parse(self, response):
        hdoc = HTML(response)

        if self.latest_dt is None :
            self.latest_dt = self._latest_dt
            self.flag = True

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=30)
            self.cutoff_dt = check_date - oneweek_diff

        topic_urls = hdoc.select_urls(['//div[@class="topic_wrapper"]/div[@class="topic_data"]/a/@href'], response)

        for topic_url in topic_urls:
            topic_url = topic_url + "?content_type=articles"
            yield Request(topic_url, self.parse_topic, response)

        # episodes
        next_page = ''
        nodes = hdoc.select('//ul[@class="block-list full-directory-listing"]/li//div[@class="body info"]')
        for node in nodes:
            post_dt = textify(node.select('./p/text()'))
            post_dt = ''.join(re.findall(r'\d+/\d+/\d+', post_dt))
            post_dt = parse_date(post_dt)
            if post_dt >= self.cutoff_dt:
                url = textify(node.select('.//h3//a/@href'))
                yield Request(url, self.parse_terminal, response)
        next_page = textify(hdoc.select('//div[@class="pagination"]//span[@class="next"]/a/@href'))
        if next_page:yield Request(next_page, self.parse, response)

    def parse_topic(self, response):
        hdoc = HTML(response)

        topics = hdoc.select_urls(['//ul[@class="block-list full-directory-listing"]/li//h3/a/@href'], response)
        for topic in topics:
            yield Request(topic, self.parse_terminal, response)

        next_page = textify(hdoc.select('//div[@class="pagination"]//a[@rel="next"]/@href'))
        if next_page:
            yield Request(next_page, self.parse_topic, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)
        item = Item(response)
        posted_dt = textify(hdoc.select('//span[@class="article-data"]/text()'))
        post_dt = parse_date(posted_dt)
        if posted_dt and post_dt >= self.cutoff_dt:
            if self.flag:
                self.update_dt(post_dt)

            title = textify(hdoc.select('//h1//text()'))
            title = title.replace('\n','').replace('\t','').replace('&amp;','&')
            text = textify(hdoc.select('//span[@itemprop="description"]/p//text()')).encode('utf8').replace('ascii','ignore')
            text = re.sub(r' +',' ', text.replace('\n','').replace('\t','').replace('&amp;','&')).replace('\r','')

            author_name = textify(hdoc.select('//div[@class="page-head-meta"]/text()'))
            if "By" in author_name:
                author_name = author_name.split("| By")[-1].strip()
            else: author_name = ''

            if text:
                item.set('url', xcode(response.url))
                item.set('title', xcode(title))
                item.set('dt_added', xcode(post_dt))
                item.set('text', xcode(text))
                item.set('author.name', xcode(author_name)) if author_name else ""
                yield item.process()
