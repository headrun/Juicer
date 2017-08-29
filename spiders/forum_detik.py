from juicer.utils import *
from dateutil import parser

class Forumdetik(JuicerSpider):
    name = "forum_detik"
    start_urls = 'http://forum.detik.com/beranda-f2.html'

    def parse(self,response):
        hdoc = HTML(response)

        nodes = hdoc.select('//tbody[contains(@id,"threadbits_forum")]/tr')
        for node in nodes[:2]:
            last_date = textify(node.select('./td[@class="alt2"]/div/text()')).strip("by")
            import pdb;pdb.set_trace()
            thread_id = textify(hdoc.select('//td[contains(@id,"td_threadtitle_")]/@id')).split('_')[-1]
            date_added = get_timestamp(parse_date(xcode(last_date)) - datetime.timedelta(hours=9))
            thread_links = textify(node.select('./td[@class="alt2"]//img[contains(@alt,"Go to last post")]/parent::a/@href'))
            if 'http' not in thread_links: thread_links = 'http://forum.detik.com/' + thread_links
            if last_date >= get_current_timestamp()-86400*30: yield Request(thread_links,self.parse_next,response,meta={'thread_id':thread_id})

        next_page = hdoc.select('//a[@rel="next"]/@href').extract()[0]
        if 'http' not in next_page:
            next_page = 'http://forum.detik.com/' + next_page
            yield Request(next_page,self.parse,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//td[@class="navbar"]/strong/text()'))
        comments = hdoc.select('//div[@id="posts"]//div[contains(@id,"edit")]')
        forum_name = textify(hdoc.select('//span[@class="navbar"]/a/text()').extract()[-1])
        forum_url = textify(hdoc.select('//span[@class="navbar"]/a/@href').extract()[-1])
        if 'http' not in forum_url: forum_url = 'http://forum.detik.com/' + forum_url
        forum_id = textify(forum_url.split('-')[-1]).split('.html')[0]
        for comment in comments:
            comment_id = textify(comment.select('./table[@class="tborder"]/@id'))
            author = textify(comment.select('.//a[@class="bigusername"]/text()'))
            author_url = textify(comment.select('.//a[@class="bigusername"]/@href'))
            if 'http' not in author_url: author_url = 'http://forum.detik.com/' + author_url
            other_info = comment.select('.//td[@class="alt2"]/div[@class="smallfont"]//text()').extract()
            date = ' '.join(textify(comment.select('.//td[@class="thead"]/text()')).split(' ')[0:-1])
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if  date < get_current_timestamp()-86400*30:
                is_next = False
                continue
            text = textify(comment.select('.//td[contains(@id,"td_post")]/div[contains(@id,"post_message")]//text()'))
            thread = {'url':xcode(response.url),'id':response.meta['thread_id'],'name':xcode(title)}
            author_info = []
            for i in other_info:
                i = textify(str(xcode(i)).strip('\n\t\r')).strip(' ')
                if i != '':author_info.append(str(i))

            item = Item(response)
            item.set('url',response.url + '#' + comment_id)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('forum',{'name':forum_name,'id':forum_id,'url':forum_url})
            item.set('thread',thread)
            item.set('author',{'name':xcode(author),'url':author_url,'info':xcode(author_info)})
            item.set('xtags',['forums_sourcetype_manual','indonesia _country_manual'])
            #yield item.process()

        try:nxt_page = textify(hdoc.select('//a[contains(@title,"Prev Page")]/@href').extract()[0])
        except:nxt_page = ''
        if nxt_page != '' and is_next:
            nxt_page = 'http://forum.detik.com/' + nxt_page
            yield Request(nxt_page,self.parse_next,response,meta={'thread_id':response.meta['thread_id']})
