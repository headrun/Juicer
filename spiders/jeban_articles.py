from juicer.utils import *
from dateutil import parser
import json
from scrapy.http import TextResponse

class JebanArticles(JuicerSpider):
    name = 'jeban_articles'
    start_urls = ['http://jeban.com/prspecial.php','http://jeban.com/activities_list.php?page=1&f=18','http://jeban.com/activity_reviews.php','http://jeban.com/prnews.php','http://jeban.com/beautynews.php']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False

    def parse(self,response):
        hdoc = HTML(response)

        if self.latest_dt is None :
            self.latest_dt = self._latest_dt
            self.flag = True

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select('//h4/a[@title]/@href').extract() or hdoc.select('//a[@class="head"]/@href').extract()

        for node in nodes[:2]:
            if 'http' not in node: node = 'http://jeban.com/' + node
            yield Request(node,self.details,response)

        next_pg = textify(hdoc.select('//div[@class="pull-right"]//i[@class="fa fa-toggle-right"]/parent::a/@href'))
        if next_pg:
            next_pg = 'http://jeban.com/' + next_pg
            yield Request(next_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@data-topic-id]//h1/text()'))
        posted_by = textify(hdoc.select('//li[@class="topic-info-poster"]//strong/text()'))
        posted_byurl = textify(hdoc.select('//li[@class="topic-info-poster"]//a/@href'))
        if 'http' not in posted_byurl: posted_byurl = 'http://jeban.com/' + posted_byurl
        author_details = {'name':xcode(posted_by),'url':xcode(posted_byurl)}
        posted_on = textify(hdoc.select('//li[@class="topic-time"]/a/@title'))
        posted_added = parse_date(posted_on)
        date_added = get_timestamp(parse_date(xcode(posted_on)) - datetime.timedelta(hours=7))
        text = textify(hdoc.select('//div[@class="post-block"]//div[@dir="ltr"]//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',date_added)
        item.set('author',author_details)
        item.set('text',xcode(text))
        #yield item.process()

        print response.url
        print 'title',xcode(title)
        print 'posted_by',xcode(author_details)
        print 'dt_adde',date_added

        try: url_id = response.url.split('?t=')[1]
        except: url_id = ''
        url = ['http://jeban.com/2014/ajax/topic/replies_after.php?t=%s&latest_post=&latest_no=&limit=0'%url_id]
        if posted_added >= self.cutoff_dt and url : yield Request(url,self.parse_details,response,meta={'response.url':response.url})

    def parse_details(self,response):
        hdoc = HTML(response)
        body = json.loads(response.body)
        import pdb;pdb.set_trace()
        val = xcode(body['Replies_HTML'])
        if val:
            print '-----------------'
            res = TextResponse(url=response.url, body=val)
            hdoc = HTML(res)
            response.url = response.meta['response.url']
            threads = hdoc.select('//div[contains(@class,"panel panel-default reply")]')

            for thread in threads:
                _id = textify(thread.select('./@data-post-id'))
                comment_number = textify(thread.select('.//ul[@class="list-inline navbar-left navbar-text hidden-xs"]//span[@class="label label-default"]/text()'))
                date = textify(thread.select('.//i[@class="fa fa-clock-o"]/parent::li/@title'))
                dt_added  = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
                author_name = textify(thread.select('.//i[@class="fa fa-at"]/parent::li/a/text()'))
                author_url = textify(thread.select('.//i[@class="fa fa-at"]/parent::li/a/@href'))
                comment = textify(thread.select('.//div[@class="reply-text"]//text()'))
                if 'http' not in author_url: author_url = 'http://jeban.com/' + author_url
                author_info = {'name':xcode(author_name),'url':xcode(author_url)}
                sk = _id + xcode(comment) + xcode(author_name)

                item = Item(response)
                import pdb;pdb.set_trace()
                item.set('url',response.url)
                item.set('_id',_id)
                item.set('comment_number',xcode(comment_number))
                item.set('dt_added',xcode(dt_added))
                item.set('author_name',xcode(author_name))
                item.set('comment',xcode(comment))
                item.set('sk',md5(sk))
                #yield item.process()
