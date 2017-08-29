from juicer.utils import *
from dateutil import parser

class CaravanersForum(JuicerSpider):
    name = 'caravaners_forum'
    start_urls = ['http://caravanersforum.com/']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//dl[contains(@class, "icon forum_read")]//a[@class="forumtitle"]/@href').extract()
        for link in links:
            import pdb;pdb.set_trace()
            if 'http' not in link: link = 'http://caravanersforum.com' + link.strip('.')
            yield Request(link,self.parse_next,response)
    
    def parse_next(self,response):
        hdoc = HTML(response)
        forum_title = textify(hdoc.select('//h2[@class="forum-title"]/a/text()'))
        forum_id = response.url.split('.php?f=')[-1].split('&')[0]
        forum = {'name':xcode(forum_title),'url':response.url,'id':forum_id}
        forum_links = hdoc.select('//ul[@class="topiclist topics"]//dd[@class="lastpost"]')

        for forum_link in forum_links:
            date = textify(forum_link.select('./span/text()')).strip('by')
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=10))
            if date_added < get_current_timestamp()-86400*30:
                continue
            forumlink = textify(forum_link.select('.//a[@title="Go to last post"]/@href'))
            if 'http' not in forumlink: forumlink = 'http://caravanersforum.com' + forumlink.strip('.')
            yield Request(forumlink,self.parse_details,response,meta={'forum':forum})

        next_page = hdoc.select('//li[@class="next"]/a[@rel="next"]/@href').extract()
        if next_page:
            next_page =  'http://caravanersforum.com' + (next_page[0].strip('.'))
            yield Request(next_page,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//h2[@class="topic-title"]/a/text()'))
        thread_url = textify(hdoc.select('//h2[@class="topic-title"]/a/@href'))
        thread_id = thread_url.split('&t=')[-1].split('&')[0]
        if 'http' not in thread_url : thread_url = 'http://caravanersforum.com' + thread_url.strip('.')
        nodes = hdoc.select('//div[@id="page-body"]/div[contains(@class,"post has-profile")]')

        for node in nodes:
            comment_id = textify(node.select('./@id'))
            author = textify(node.select('.//p[@class="author"]/span/strong/a/text()'))
            author_url = textify(node.select('.//p[@class="author"]/span/strong/a/@href'))
            if 'http' not in author_url: author_url = 'http://caravanersforum.com' + author_url.strip('.')
            dt = textify(node.select('.//p[@class="author"]/text()'))
            comment = textify(node.select('.//div[@class="content"]//text()'))
            dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=10))
            sk = thread_url + '#' + comment_id
            other_info = node.select('.//dl[@class="postprofile"]/dd')
            info = []
            for i in other_info:
                x = textify(i.select('.//text()'))
                info.append(x)

            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            '''item = Item(response)
            item.set ('url',thread_url + '#' + comment_id)
            item.set('title',xcode(title))
            item.set('author',{'name':xcode(author),'url':author_url,'other_info':xcode(info)})
            items.set('dt_added',dt_added)
            item.set('text',xcode(comment))
            items.set('forum',response.meta['forum'])
            item.set('thread',{'name':xcode(title),'url':thread_url,'id':thread_id})
            item.set('sk',md5(sk))
            yield item.process()
        nxt_pg = hdoc.select('//li[@class="previous"]/a/@href').extract()
        if nxt_pg and is_next:
            nxt_pg = 'http://caravanersforum.com' + nxt_pg.strip('.')
            yield Request(nxt_pg,self.parse_details,response,meta={'forum':response.meta['forum']}'''
