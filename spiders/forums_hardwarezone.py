from juicer.utils import *
from dateutil import parser

class HardwairezoneForum(JuicerSpider):
    name ='forums_hardwarezone'
    start_urls =['http://forums.hardwarezone.com.sg/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        forum_list = hdoc.select('//tbody[contains(@id,"collapseobj_forumbit")]/tr')
        for link in forum_list:
            forum_date = textify(link.select('.//span[@class="time"]/parent::div/text()'))
            forum_dt_added = get_timestamp(parse_date(xcode(forum_date),dayfirst=True) - datetime.timedelta(hours=8))
            if forum_dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            links = link.select('.//td[@class="alt1Active"]/div/a/@href').extract()
            for link in links:
                if 'http' not in link: link = 'http://forums.hardwarezone.com.sg' + link
                if link and is_next:yield Request(link, self.parse_next, response)

    def parse_next(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//tbody[contains(@id,"threadbits_forum")]/tr')
        for node in nodes:
            threadlink = textify(node.select('.//img[@alt="Go to last post"]/parent::a/@href'))
            date = textify(node.select('./td[@class="alt2"]/div[@class="smallfont"]/text()'))
            if 'by' in date:date = date.split('by')[0].strip(' ')
            date_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                continue
            if 'http:' not in threadlink:
                threadlink = 'http://forums.hardwarezone.com.sg'+ threadlink
            yield Request(threadlink, self.final_comments, response)

        next_page = hdoc.select('//div[@class="pagination"]/ul/li[@class="prevnext"]/a[contains(@title,"Next")]/@href').extract() or hdoc.select('//div[@class="pagination"]//li[@class="prevnext"]/a[contains(@title,"Next Page")]/@href').extract()
        
        if next_page:
            next_page = 'http://forums.hardwarezone.com.sg' + next_page[0]
            yield Request(next_page,self.parse_next,response)

    def final_comments(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//h2[@class="header-gray"]/text()').extract())
        try:thread_id = textify(hdoc.select('//td[@class="vbmenu_control"]/@title').extract()[0]).split('t=')[-1]
        except:
            thread_id = response.url.split('-')[-1].split('.html')[0]
        forum_url = textify(hdoc.select('//a[@class="rss"]/parent::li/preceding-sibling::li[1]/a/@href'))
        if 'http:' not in forum_url:
            forum_url = 'http://forums.hardwarezone.com.sg'+ forum_url
        forum_id = forum_url.split('-')[-1].strip('/')
        forum_title = textify(hdoc.select('//a[@class="rss"]/parent::li/preceding-sibling::li[1]/a/text()'))
        comments_listing = hdoc.select('//div[@class="post-wrapper"]')
        for comment_list in comments_listing:
            date = textify(comment_list.select('.//a[contains(@name,"post")]/parent::td/text()'))
            dt_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=8))
            user_name = textify(comment_list.select('.//a[@class="bigusername"]/text()'))
            user_url = textify(comment_list.select('.//a[@class="bigusername"]/@href'))
            if 'http:' not in user_url:
                user_url = 'http://forums.hardwarezone.com.sg'+ user_url
            text = textify(comment_list.select('.//td[contains(@id,"td_post")]//text()'))
            extra_text = textify(comment_list.select('.//td[@class="alt1 systemrigfont"]/div//text()'))
            text = text + extra_text
            auth_info = comment_list.select('.//a[@class="bigusername"]/parent::div/following-sibling::div//text()').extract()
            author_info = []
            for info in auth_info:
                if textify(info) != '':author_info.append(str(textify(info)))
            comment_id = textify(comment_list.select('./table[contains(@id,"post")]/@id'))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            sk = xcode(title) + comment_id
            item = Item(response)
            item.set('url',response.url + '#' + comment_id)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('author',{'name':xcode(user_name),'url':user_url,'other_info':author_info})
            item.set('thread',{'title':xcode(title),'id':str(thread_id),'url':response.url})
            item.set('forum',{'title':xcode(forum_title),'id':str(forum_id),'url':forum_url})
            item.set('text',xcode(text))
            item.set('sk',md5(sk))
            item.set('xtags',['singapore_country_manual', 'forums_sourcetype_manual'])
            yield item.process()

        nxt_page = hdoc.select('//div[@class="pagination"]/ul/li[@class="prevnext"]/a[contains(@title,"Prev")]/@href').extract() or hdoc.select('//div[@class="pagination"]//li[@class="prevnext"]/a[contains(@title,"Next Page")]/@href').extract()
        if nxt_page and is_next:
            if 'http' not in nxt_page: nxt_page = 'http://forums.hardwarezone.com.sg' + nxt_page[0]
            yield Request(nxt_page, self.final_comments, response)
