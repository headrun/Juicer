from juicer.utils import *
from dateutil import parser

class ExpansysForum(JuicerSpider):
    name = 'expansys_forum'
    start_urls = ['http://www.expansys.com.sg/forums/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//div[@id="listing"]//tbody//tr')
        for link in links:
            date = textify(link.select('./td[@class="last"]/p/text()')).strip('by on')
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            url = textify(link.select('./td[@class="first"]/h2/a/@href'))
            if 'http' not in url: url = 'http://www.expansys.com.sg' + url
            yield Request(url,self.parse_details,response)

        next_page = textify(hdoc.select('//li[@class="next"]/a/@href').extract()[0])
        if next_page and is_next:
            next_page = 'http://www.expansys.com.sg' + next_page
            yield Request(next_page,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        forum_name = textify(hdoc.select('//ul[@id="breadcrumbs"]/li[@class="level_2"]/a/text()'))
        forum_url = textify(hdoc.select('//ul[@id="breadcrumbs"]/li[@class="level_2"]/a/@href'))
        if 'http' not in forum_url: forum_url = 'http://www.expansys.com.sg' + forum_url
        forum_id = forum_url.split('?i=')[-1]
        thread_id = response.url.split('?k=')[-1]
        title = textify(hdoc.select('//table[@class="forumTable viewThreadTable"]/thead//h1/text()'))
        node1 = hdoc.select('//table[@class="forumTable viewThreadTable"]/tbody/tr[@class="info"]')
        node2 = hdoc.select('//table[@class="forumTable viewThreadTable"]/tbody/tr[@class="post"]')

        for x,y in zip(node1,node2):
            dt = x.select('.//td[@class="date"]/strong/text()').extract()[0]
            dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
            region = x.select('.//td[@class="date"]/strong/text()').extract()[1]
            author = textify(y.select('.//td/ul[@class="user"]/li[@class="name"]/a/text()'))
            author_url = textify(y.select('.//td/ul[@class="user"]/li[@class="name"]/a/@href'))
            if 'http' not in author_url : author_url = 'http://www.expansys.com.sg' + author_url
            noof_posts = textify(y.select('.//li[@class="posts"]/text()'))
            joined_on = textify(y.select('.//li[@class="joined"]/strong/text()'))
            text = textify(y.select('.//td[@class="last"]/p//text()'))
            comment_count = textify(x.select('.//td[@class="count"]/text()'))
            other_info = {'no.ofposts':noof_posts,'joined_on':joined_on,'region':region}
            sk = response.url + comment_count

            if dt_added < get_current_timestamp()-86400*30:
                continue

            item = Item(response)
            item.set('url',response.url + comment_count)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('author',{'name':xcode(author),'url':author_url,'other_info':other_info})
            item.set('text',xcode(text))
            item.set('forum',{'name':xcode(forum_name),'url':forum_url,'id':forum_id})
            item.set('thread',{'name':xcode(title),'url':response.url,'id':thread_id})
            item.set('sk',md5(sk))
            item.set('xtags',['forums_sourcetype_manual','singapore_country_manual'])
            yield item.process() 
