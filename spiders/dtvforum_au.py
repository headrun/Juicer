from juicer.utils import *
from dateutil import parser

class DtvForum(JuicerSpider):
    name  = 'dtvforum_au'
    start_urls = ['http://www.dtvforum.info/index.php/forum/158-hd-3d-smart-tvs/']

    def parse(self,response):
        hdoc = HTML(response)
        thread_links = hdoc.select('//tr[@data-tid]//ul[contains(@class,"last_post")]')
        for thread_link in thread_links[:4]:
            threadlink = textify(thread_link.select('./li/a/@href'))
            date = textify(thread_link.select('./li/a/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=10))
            if date_added < get_current_timestamp()-86400*30:
                continue
            yield Request(threadlink,self.parse_next,response)

        next_page = hdoc.select('//li[@class="next"]/a/@href').extract()
        if next_page:
            next_page = next_page[0]
            yield Request(next_page,self.parse,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="name"]/text()'))
        forum_name = hdoc.select('//a/span[@itemprop="title"]/text()').extract()[-1]
        forum_url = hdoc.select('//span[@itemprop="title"]/parent::a/@href').extract()[-1]
        forum_id = forum_url.split('forum/')[-1].split('-')[0]
        thread_id = response.url.split('topic/')[-1].split('-')[0]

        nodes = hdoc.select('//div[contains(@class,"post_block")]')
        for node in nodes:
            comment_id = textify(node.select('./a/@id'))
            author_name = textify(node.select('.//span[@itemprop="creator name"]/text()'))
            other_info = textify(node.select('.//ul[@class="basic_info"]//text()'))
            dt = textify(node.select('.//abbr[@itemprop="commentTime"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=10))
            comment = textify(node.select('.//div[@itemprop="commentText"]//p[not(contains(@class,"edit"))]//text()'))
            forum = {'name':xcode(forum_name),'url':forum_url,'id':forum_id}
            thread = {'name':xcode(title),'url':response.url,'id':thread_id}

            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            print '\n'
            print response.url + '#' + comment_id
            print 'title',xcode(title)
            print 'author',{'name':xcode(author_name),'other_info':xcode(other_info)}
            print 'dt_added',dt_added
            print 'text',xcode(comment)
            print 'forum',forum
            print 'thread',thread

        nxt_pg = hdoc.select('//li[@class="prev"]/a/@href').extract()
        if nxt_pg:
            nxt_pg = nxt_pg[0]
            yield Request(nxt_pg,self.parse_next,response)
