from juicer.utils import *
from dateutil import parser

class TeamBhp(JuicerSpider):
    name = 'teambhp'
    start_urls = ['http://www.team-bhp.com/forum/']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//td[@class="alt1Active"]')
        for link in links:
            forum_id = textify(link.select('./@id'))
            threadlinks = link.select('.//div/a/@href').extract()
            for threadlink in threadlinks:
                yield Request(threadlink,self.parse_forum,response,meta={'forum_id':forum_id})

    def parse_forum(self,response):
        hdoc = HTML(response)
        threads = hdoc.select('//td[contains(@id,"td_threadtitle")]/parent::tr')

        for thread in threads[:1]:
            dt = textify(thread.select('.//span[@class="time"]/parent::div/text() | .//span[@class="time"]/text()'))
            date_added = get_timestamp(parse_date(dt)-datetime.timedelta(hours=5 , minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                continue
            post_link = textify(thread.select('.//img[@alt="Go to last post"]/parent::a/@href'))
            yield Request(post_link, self.parse_details, response,meta={'forum_id':response.meta['forum_id']})

        nxt_pg = hdoc.select('//a[contains(@title, "Next Page - Results")]/@href').extract()
        if nxt_pg:
            nxt_pg = textify(nxt_pg[0])
            yield Request(nxt_pg, self.parse_forum,response,meta={'forum_id':response.meta['forum_id']})

    def parse_details(self,response):
        hdoc = HTML(response)
        is_next = True
        forum_name = textify(hdoc.select('//span[@class="navbar"][last()]/a/text()'))
        forum_url = textify(hdoc.select('//span[@class="navbar"][last()]/a/@href'))
        title = textify(hdoc.select('//h1[@class="myh1"]/text()'))
        thread_id = response.url.split('/')[-1].split('-')[0]

        nodes = hdoc.select('//div[contains(@id,"edit")]')

        for node in nodes:
            date = textify(node.select('.//a[contains(@name,"post")]/parent::td/text()'))
            dt_added = get_timestamp(parse_date(date)-datetime.timedelta(hours=5, minutes=30))
            if dt_added < get_current_timestamp()-864000*30:
                is_next = False
                continue
            author = textify(node.select('.//a[@class="bigusername"]/text()'))
            author_url = textify(node.select('.//a[@class="bigusername"]/@href'))
            other_info = node.select('.//div[contains(@id,"postmenu")]/parent::td//div[@class="smallfont"]//text()').extract()
            text = textify(node.select('.//div[contains(@id,"post_message")]//text()'))
            comment_id = textify(node.select('.//div[contains(@id,"post_message")]/@id'))
            comment_id = textify(re.findall('\d+',comment_id))
            auth_info = []
            for info in other_info:
                if textify(info) != '':auth_info.append(str(info).strip())
            sk = comment_id

            item = Item(response)
            item.set('url', response.url + '#post' + comment_id)
            item.set('title',xcode(title))
            item.set('dt_added', dt_added)
            item.set('thread',{'title':xcode(title), 'url':response.url, 'id':thread_id})
            item.set('forum',{'title':xcode(forum_name), 'url':forum_url, 'id':response.meta['forum_id']})
            item.set('author',{'name':xcode(author), 'url':author_url, 'other_info':xcode(auth_info)})
            item.set('text',xcode(text))
            item.set('sk', md5(sk))

        next_pg = hdoc.select('//a[contains(@title, "Prev Page - Results")]/@href').extract()
        if next_pg and is_next:
            next_pg = next_pg[0]
            yield Request(next_pg, self.parse_details, response, meta={'forum_id`':response.meta['forum_id']})

