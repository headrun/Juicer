from juicer.utils import *
from dateutil import parser

class PropertyrealestateForum(JuicerSpider):
    name = "propertyrealestate_forum"
    start_urls = ['http://www.propertyrealestateforum.com/forum/forum.php']

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

        links = hdoc.select('//h2[@class="forumtitle"]/a/@href').extract()

        for link in links[:2]:
            if 'http' not in link: link = 'http://www.propertyrealestateforum.com/forum/' + link
            yield Request(link,self.parse_threads,response)

    def parse_threads(self,response):
        hdoc = HTML(response)
        forum_id = ''.join(response.url.split('-')[0]).split('/')[-1]
        forum_title = textify(hdoc.select('//span[@class="forumtitle"]'))
        forum = {'forum_id':forum_id,'forum_url':response.url,'forum_title':forum_title}
        nodes = hdoc.select('//dl[@class="threadlastpost td"]//a[@title="Go to last post"]/@href').extract()
        for node in nodes:
            if 'http' not in node: node = 'http://www.propertyrealestateforum.com/forum/' + node
            yield Request(node,self.parse_details,response,meta={'forum':forum})

        next_page = textify(hdoc.select('//div[@id="below_threadlist"]//a[@rel="next"]/@href'))
        if next_page:
            if 'http' not in next_page: next_page = 'http://www.propertyrealestateforum.com/forum/' + next_page
            yield Request(next_page,self.parse_threads,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        forum = response.meta['forum']
        thread_id = ''.join(response.url.split('-')[0]).split('/')[-1]
        title = textify(hdoc.select('//span[@class="threadtitle"]/a/text()'))
        info = hdoc.select('//ol[@id="posts"]/li[contains(@id,"post_")]')

        for inf in info:
            date = textify(inf.select('.//span[@class="postdate old"]//text()'))
            date1 = parse_date(xcode(date))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date1 < self.cutoff_dt:
                continue
            _id = textify(inf.select('./@id'))
            text = textify(inf.select('.//div[@class="content"]//blockquote[@class="postcontent restore "]//text()'))
            author_name = textify(inf.select('.//div[@class="popupmenu memberaction"]/a//text()')) or textify(inf.select('.//span[@class="username guest"]/text()'))
            author_url = textify(inf.select('.//div[@class="popupmenu memberaction"]/a/@href'))
            author_title = textify(inf.select('.//span[@class="usertitle"]/text()'))
            author_otherinfo = textify(inf.select('.//dl[@class="userinfo_extra"]//text()'))

            print '\n'
            print 'url',response.url + '#' +_id
            print 'title',xcode(title)
            print 'author',{'name':author_name,'url':author_url,'tilte':author_title,'other_info':author_otherinfo}
            print 'dt_added',dt_added
            print 'text',xcode(text)
            print 'forum',forum
            print 'thread',{'thread_id':thread_id,'thread_url':response.url,'thread_title':title}
