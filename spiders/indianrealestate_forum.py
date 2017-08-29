from juicer.utils import *
from dateutil import parser

class IndianRealestateForum(JuicerSpider):
    name = 'indianrealestate_forum'
    start_urls = ['http://www.indianrealestateboard.com/forums/forum.php']

    def parse(self,response):
        hdoc  = HTML(response)
        links = hdoc.select('//h2[@class="forumtitle"]/a/@href | //li[@class="subforum"]/a/@href').extract()
        for link in links:
            if 'http' not in link:link = 'http://www.indianrealestateboard.com/forums/' + link
            yield Request(link,self.parse_threads,response)#,meta={'dont_redirect':True,'handle_httpstatus_list':[302]})

    def parse_threads(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//dl[@class="threadlastpost td"]')
        for node in nodes:
            date = textify(node.select('.//span[@class="time"]/parent::dd//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            thread_link = textify(node.select('.//a[@title="Go to last post"]/@href'))
            if 'http' not in thread_link: thread_link = 'http://www.indianrealestateboard.com/forums/' + thread_link
            yield Request(thread_link,self.details,response)

        nxt_page = hdoc.select('//a[@rel="next"]/@href').extract()
        if nxt_page and is_next:
            nxt_page = 'http://www.indianrealestateboard.com/forums/' + nxt_page[0]
            yield Request(nxt_page,self.parse_threads,response)

    def details(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//span[@class="threadtitle"]/a/text()'))
        thread_id = response.url.split('/')[-1].split('-')[0]
        thread_url = textify(hdoc.select('//span[@class="threadtitle"]/a/@href'))
        forum_url = textify(hdoc.select('//li[@class="navbit"]/a/@href').extract()[-1])
        if 'http' not in forum_url:forum_url = 'http://www.indianrealestateboard.com/forums/' + forum_url
        forum_title = textify(hdoc.select('//li[@class="navbit"]/a/text()').extract()[-1])
        forum_id = forum_url.split('/')[-1].split('-')[0]
        threads = hdoc.select('//div[@class="postdetails_noavatar"]/parent::li[contains(@id,"post_")]')
        for thread in threads:
            dt = textify(thread.select('.//span[@class="date"]//text()'))
            dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=5,minutes=30))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            author_name = textify(thread.select('.//div[@class="username_container"]//strong/span/text()'))
            author_url = textify(thread.select('.//a[@class="siteicon_profile"]/@href'))
            if 'http' not in author_url: author_url = 'http://www.indianrealestateboard.com/forums/' + author_url
            comment = textify(thread.select('.//div[contains(@class,"content")]//text()'))
            comment_id = textify(thread.select('./@id'))
            sk = thread_url+comment_id

            item = Item(response)
            item.set('url',response.url +'#' + comment_id)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('author',{'name':xcode(author_name),'url':xcode(author_url)})
            item.set('thread',{'name':xcode(title),'url':response.url,'id':thread_id})
            item.set('forum',{'name':xcode(forum_title),'url':forum_url,'id':forum_id})
            item.set('text',xcode(comment))
            yield item.process()

        next_pg = hdoc.select('//a[@rel="prev"]/@href').extract()
        if next_pg and is_next:
            next_pg = 'http://www.indianrealestateboard.com/forums/' + next_pg[0]
            yield Request(next_pg,self.details,response)
