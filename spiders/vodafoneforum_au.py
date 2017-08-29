from juicer.utils import *
from dateutil import parser

class VodafoneForum(JuicerSpider):
    name = 'vodafone_forum'
    start_urls = ['http://community.vodafone.com.au/t5/forums/recentpostspage/post-type/message']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//tr//div[@class="MessageSubjectCell"]')

        for link in links:
            thread_link = textify(link.select('.//h2[@class="message-subject"]//a/@href'))
            if 'http' not in thread_link: thread_link = 'http://community.vodafone.com.au' + thread_link
            date = textify(link.select('.//span[@class="DateTime"]/span/@title')).strip(u'\u200e')
            date_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=10))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            yield Request(thread_link,self.parse_next,response)

        next_page = textify(hdoc.select('//a[@rel="next"]/@href'))
        if next_page and is_next:
            if 'http' not in next_page: next_page = 'http://community.vodafone.com.au' + next_page
            yield Request(next_page,self.parse,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//h1[@class="lia-forum-topic-subject"]/text()'))
        forum_title = textify(hdoc.select('//a[@id="link_2"]/text()'))
        forum_url = textify(hdoc.select('//a[@id="link_2"]/@href'))
        if 'http' not in forum_url: forum_url = 'http://community.vodafone.com.au' + forum_url
        thread_id = textify(hdoc.select('//title/text()')).split('-')[-1]
        nodes = hdoc.select('//div[contains(@id,"lineardisplaymessageviewwrapper")]')

        for node in nodes:
            comment_id = textify(node.select('.//div/@data-message-id'))
            dt = node.select('.//p[contains(@class,"lia-message-dates")]//span[@class="local-friendly-date"]/@title').extract() or node.select('.//p[contains(@class,"lia-message-dates")]//span[@class="local-date"]/text() | .//p[contains(@class,"lia-message-dates")]//span[@class="local-time"]/text()').extract()
            if len(dt) == 2:dt = textify(dt[0]).strip(u'\u200e')
            else: dt = textify(dt).strip(u'\u200e')
            dt_added = get_timestamp(parse_date(xcode(dt),dayfirst=True) - datetime.timedelta(hours=10))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            comment = textify(node.select('.//div[@class="lia-message-body-content"]/*[not(contains(@class,"UserSignature lia-message-signature"))]//text() | .//div[@class="lia-message-body-content"]/text()'))
            comment_url = textify(node.select('.//li/a[contains(@id,"highlightMessage")]/@href'))
            if 'http' not in comment_url: comment_url = 'http://community.vodafone.com.au' + comment_url
            author_name = textify(node.select('.//span[@class="UserName lia-user-name"]/a//text()'))
            author_url = textify(node.select('.//span[@class="UserName lia-user-name"]/a/@href'))
            sk = 'http://community.vodafone.com.au' + comment_url

            item = Item(response)
            item.set('url',comment_url)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('forum',{'name':xcode(forum_title),'url':forum_url})
            item.set('thread',{'id':thread_id,'url':response.url,'name':xcode(title)})
            item.set('author',{'name':author_name,'url':author_url})
            item.set('text',xcode(comment))
            item.set('sk',md5(sk))
            item.set('xtags',['forums_sourcetype_manual','australia_country_manual'])
            yield item.process()

        nxt_pg = textify(hdoc.select('//a[@rel="prev"]/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg: nxt_pg = 'http://community.vodafone.com.au' + nxt_pg
            yield Request(nxt_pg,self.parse_next,response)
