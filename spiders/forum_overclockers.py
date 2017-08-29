from juicer.utils import *
from dateutil import parser

class ForumOverclockers(JuicerSpider):
    name = 'forum_overclockers'
    start_urls = ['http://forums.overclockers.com.au/forumdisplay.php?f=94','http://forums.overclockers.com.au/forumdisplay.php?f=98','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=7','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=8','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=6','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=23','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=52','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=24','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=73','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=99','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=25','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=50','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=26','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=32','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=44','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=68','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=58','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=92','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=21','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=22','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=63','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=28','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=39','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=40','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=42','http://forums.overclockers.com.au/forumdisplay.php?f=83','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=41','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=9','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=11','http://forums.overclockers.com.au/forumdisplay.php?f=90','http://forums.overclockers.com.au/forumdisplay.php?f=79','http://forums.overclockers.com.au/forumdisplay.php?f=80','http://forums.overclockers.com.au/forumdisplay.php?f=78','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=61','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=30','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=65','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=72','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=86','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=96','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=46','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=93','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=94','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=74','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=27','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=67','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=48','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=64','http://forums.overclockers.com.au/forumdisplay.php?s=5c0a1c225abf8c5268fb50849018e5c0&f=75']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//tr//td[contains(@title,"Replies:")]')
        for link in links[:4]:
            date=textify(link.select('.//span[@class="time"]/parent::div/text() | .//span[@class="time"]/text()')).split('by')[0]
            import pdb;pdb.set_trace()
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=10))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            threadlink = textify(link.select('.//img[@alt="Go to last post"]/parent::a/@href'))
            if 'http' not in threadlink:threadlink = 'http://forums.overclockers.com.au/' + threadlink
            yield Request(threadlink,self.parse_next,response)

        next_page = hdoc.select('//a[@rel="next"]/@href').extract()
        if next_page and is_next:
            next_page = 'http://forums.overclockers.com.au/' + next_page[0]
            yield Request(next_page,self.parse,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        forum_name = hdoc.select('//tr[@valign="bottom"]//span[@class="navbar"]/a/text()').extract()[-1]
        forum_url = hdoc.select('//tr[@valign="bottom"]//span[@class="navbar"]/a/@href').extract()[-1]
        forum_id = forum_url.split('f=')[-1]
        if 'http' not in forum_url:forum_url = 'http://forums.overclockers.com.au/' + forum_url
        title = textify(hdoc.select('//td[@class="navbar"]/strong/text()'))
        thread_id = hdoc.select('//a[@rel="start"]/@href').extract()[0].split('t=')[-1]
        nodes = hdoc.select('//div[@align="center"]//table[contains(@id,"post")]')

        for node in nodes:
            comment_id = textify(node.select('./@id'))
            dt = textify(node.select('.//a[contains(@name,"post")]/parent::td[@class="thead"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=10))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            name = textify(node.select('.//a[@class="bigusername"]/text()'))
            url = textify(node.select('.//a[@class="bigusername"]/@href'))
            comment = textify(node.select('.//td[contains(@id,"td_post_")]/div[contains(@id,"post_message")]//text()'))
            other_info = node.select('.//div[contains(@id,"postmenu")]/parent::td/div[@class="smallfont"]')
            auth_info = []
            for i in other_info:
                x = textify(i.select('.//text()'))
                if x != '':auth_info.append(x)
            sk = 'http://forums.overclockers.com.au/showthread.php?t=%s'%thread_id + '&p=' + comment_id.strip('post')
            item = Item(response)
            item.set('http://forums.overclockers.com.au/showthread.php?t=%s'%thread_id + '&p=' + comment_id.strip('post'))
            item.set('title',xcode(title))
            item.set('author',{'url':url,'name':xcode(name),'other_info':auth_info})
            item.set('dt_added',dt_added)
            item.set('comment',xcode(comment))
            item.set('forum',{'name':xcode(forum_name),'url':forum_url,'id':forum_id})
            item.set('thread',{'name':xcode(title),'url':response.url,'id':thread_id})
            item.set('sk',md5(sk))
            item.set('xtags',['forums_sourcetype_manual','australia_country_manual'])
            yield item.process()

        nxt_pg = hdoc.select('//a[@rel="prev"]/@href').extract()
        if nxt_pg and is_nxt:
            nxt_pg = 'http://forums.overclockers.com.au/' + nxt_pg[0]
            yield Request(nxt_pg,self.parse_next,response)
