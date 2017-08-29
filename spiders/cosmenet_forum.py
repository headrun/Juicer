from juicer.utils import *
from dateutil import parser

class CosmenetForum(JuicerSpider):
    name = 'cosmenet_forum'
    start_urls = ['http://www.cosmenet.in.th/webboard/']

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
            check_date = self._latest_dt + datetime.timedelta(hours=7)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select('//span[@class="forum-item-title"]/a/@href').extract()

        for node in nodes:
            if 'http' not in node: node = 'http://www.cosmenet.in.th' + xcode(node)
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        forum_title = textify(hdoc.select('//h1[@class="title-content"]/text()'))
        forum_id = textify(re.findall('forum\d',response.url))
        forum = {'forum_id':forum_id ,'forum_url':response.url ,'forum_title':forum_title}
        thread_links = hdoc.select('//tr[contains(@class,"forum-")]')

        for thread_link in thread_links:
            link = textify(thread_link.select('.//span[@class="forum-item-pages"]/noindex[last()]/a/@href')) or textify(thread_link.select('.//span[@class="forum-item-title"]/a/@href'))
            thread_id = ''.join(textify(link.split('-')[0]).split('/')[-1])
            if 'http' not in link: link = 'http://www.cosmenet.in.th' + xcode(link)
            yield Request(link,self.details,response,meta ={'forum':forum,'thread_id':thread_id})

        next_page = textify(hdoc.select('//div[@class="forum-navigation-box forum-navigation-bottom"]//a[@class="modern-page-next"]/@href'))
        if 'http' not in next_page : next_page = 'http://www.cosmenet.in.th' + next_page
        yield Request(next_page,self.parse_next,response)

    def details(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//div[@class="forum-header-title"]/span/text()'))
        forum = response.meta['forum']
        thread_id = response.meta['thread_id']

        info = hdoc.select('//div[@class="section-post-detail"]')

        for inf in info:
            date = textify(inf.select('.//small/text()'))
            date_added = parse_date(date)
            if date_added < self.cutoff_dt:
                is_next = False
                continue
            dt_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=7))
            author_name = textify(inf.select('.//div[@class="forum-user-name"]/a/text()'))
            author_url = textify(inf.select('.//div[@class="forum-user-name"]/a/@href'))
            if 'http' not in author_url: author_url = 'http://www.cosmenet.in.th' + author_url
            author_id = textify(inf.select('.//div/@bx-author-id'))
            joined_on = textify(inf.select('.//span[contains(text(),"Joined")]/span/text()'))
            joined_dt_added = get_timestamp(parse_date(xcode(joined_on),dayfirst=True) - datetime.timedelta(hours=7))
            number_of_posts = textify(inf.select('.//span[contains(text(),"Posts")]/span//a/text()'))
            author = {'name':xcode(author_name),'url':author_url,'_id':author_id,'joined_on':joined_dt_added,'posts':number_of_posts}
            text = textify(inf.select('.//div[@class="forum-post-text"]//text()'))
            text_id = textify(inf.select('.//div[@class="forum-post-text"]/@id'))
            thread = {'thread_url':response.url,'thread_id':thread_id,'thread_title':xcode(title)}
            sk = response.url + '#' + text_id

            item = Item(response)
            item.set('url',response.url + '#' + text_id)
            item.set('title',xcode(title))
            item.set('author',author)
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('forum',forum)
            item.set('sk',md5(sk))
            yield item.process()
            print 'thread',thread

        prev_pg = textify(hdoc.select('//div[@class="forum-navigation-box forum-navigation-bottom"]//a[@class="modern-page-previous"]/@href'))
        if 'http' not in prev_pg and is_next:
            prev_pg = 'http://www.cosmenet.in.th' + prev_pg
            yield Request(prev_pg,self.details,response,meta={'forum':forum,'thread_id':thread_id})

