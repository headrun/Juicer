from juicer.utils import *
from dateutil import parser

class Xbhp(JuicerSpider):
    name = 'xbhp'
    start_urls = 'http://www.xbhp.com/talkies/forum.php'

    def parse(self,response):
        hdoc = HTML(response)
        forum_links = hdoc.select('//ol[@id="forums"]/li')

        for forum_link in forum_links:
            forum_id = textify(forum_link.select('./@id'))
            forum_id = textify(re.findall('\d+',forum_id))
            link = textify(forum_link.select('.//h2[@class="forumtitle"]/a/@href'))
            yield Request(link,self.parse_threads,response,meta={'forum_id':forum_id})

    def parse_threads(self,response):
        hdoc = HTML(response)
        threadlinks = hdoc.select('//ol[@id="stickies"]/li[contains(@id,"thread_")]')
        for threadlink in threadlinks:
            threaddate = textify(threadlink.select('.//a[@title="Go to last post"]/parent::dd/text()')).lower()
            threaddt_added = get_timestamp(parse_date(xcode(threaddate)))
            if threaddt_added < get_current_timestamp()-86400*30:
                continue
            threadurl = textify(threadlink.select('.//a[@title="Go to last post"]/@href'))
            yield Request(threadurl,self.details,response,meta={'forum_id':response.meta['forum_id']})

        thread_links = hdoc.select('//ol[@id="threads"]/li[contains(@id,"thread_")]')
        for thread_link in thread_links:
            thread_date = textify(thread_link.select('.//a[@title="Go to last post"]/parent::dd/text()')).lower()
            thread_dt_added = get_timestamp(parse_date(xcode(thread_date)))
            if thread_dt_added < get_current_timestamp()-86400*30:
                continue
            thread_url = textify(thread_link.select('.//a[@title="Go to last post"]/@href'))
            yield Request(thread_url, self.details,response,meta={'forum_id':response.meta['forum_id']})

        nxt_pg = hdoc.select('//a[@rel="next"]/@href').extract()
        if nxt_pg:
            nxt_pg = str(textify(nxt_pg[0]))
            yield Request(nxt_pg, self.parse_threads, response, meta={'forum_id':response.meta['forum_id']})

    def details(self,response):
        hdoc = HTML(response)
        is_next = True
        forum_title = textify(hdoc.select('//li[@class="navbit"]/a/text()').extract()[-1])
        forum_url = str(textify(hdoc.select('//li[@class="navbit"]/a/@href').extract()[-1]))
        title = textify(hdoc.select('//span[@class="threadtitle"]/a/text()'))
        thread_id = textify(response.url.split('/')[-1].split('-')[0])
        nodes = hdoc.select('//ol[@id="posts"]/li')
        for node in nodes:
            _id = textify(node.select('./@id'))
            date = textify(node.select('.//span[@class="date"]/text()')).lower()
            dt_added = get_timestamp(parse_date(xcode(date)))
            if dt_added < get_current_timestamp()-86400*30:
                is_continue = False
                continue
            author = textify(node.select('.//a[contains(@class,"username")]/strong//text()'))
            author_url = textify(node.select('.//a[contains(@class,"username")]/@href'))
            other_info1 = node.select('.//dl[@class="userinfo_extra"]/dt/text()').extract()
            other_info2 = node.select('.//dl[@class="userinfo_extra"]/dd/text()').extract()
            autho_info = []
            for a, b in zip(other_info1, other_info2):
                autho_info.append(str(xcode(textify(a))) + ":" + str(xcode(textify(b))))
            text = textify(node.select('.//blockquote[@class="postcontent restore "]//text()')).replace(u"\u2019", "'").replace(u'\u201d','"').replace(u'\u201c','"')
            sk = _id

            item = Item(response)
            item.set('url',response.url + '#' +  _id)
            item.set('title',xcode(title))
            item.set('dt_added', dt_added)
            item.set('forum', {'title':xcode(forum_title), 'id':response.meta['forum_id'],'url':forum_url})
            item.set('thread', {'title':xcode(title),'id':thread_id, 'url':response.url})
            item.set('author', {'name':xcode(author), 'url':author_url, 'info':xcode(autho_info)})
            item.set('text',xcode(text))
            item.set('xtags',['forums_sourcetype_manual','india_country_manual'])
            item.set('sk',md5(sk))
            yield item.process()


        next_pg = hdoc.select('//a[@rel="prev"]/@href').extract()
        if next_pg and is_next:
            next_pg = str(textify(next_pg[0]))
            yield Request(next_pg, self.details, response, meta={'forum_id':response.meta['forum_id']})
