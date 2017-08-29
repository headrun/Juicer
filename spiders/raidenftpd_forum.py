from juicer.utils import *
from dateutil import parser

class RaidenftpdForum(JuicerSpider):
    name = 'raidenftpd_forum'
    start_urls = ['http://forum.raidenftpd.com/ubbthreads.php?Cat=&C=3']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//span[@class="forumtitle"]/a/@href')
        for link in links:
            yield Request(link,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        is_next = True
        thread_links = hdoc.select('//tr[@class="lighttable"] | //tr[@class="darktable"]')
        for thread_link in thread_links:
            date = textify(thread_link.select('./td[last()]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            threadlink = textify(thread_link.select('./td[1]/a/@href'))
            yield Request(threadlink,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//img[@alt="Next page"]/parent::a/@href'))
        if nxt_pg and is_next:
            yield Request(nxt_pg,self.parse_next,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        try:title = hdoc.select('//td[@class="subjecttable"]/table[@class="subjecttable"]//b//text()').extract()[0]
        except:title = textify(hdoc.select('//td[@class="subjecttable"]/table[@class="subjecttable"]//b//text()'))
        forum_title = textify(hdoc.select('//span[@class="catandforum"]/a[last()]/text()'))
        forum_url = textify(hdoc.select('//span[@class="catandforum"]/a[last()]/@href'))
        thread_id = response.url.split('Number=')[-1].split('&')[0]
        nodes = hdoc.select('//td[@class="darktable"]')

        for node in nodes:
            comment_id = textify(node.select('./a/@name'))
            author_name = textify(node.select('./a[@href]/text()'))
            author_url = textify(node.select('./a[@href]/@href'))
            if 'http' not in author_url: author_url = 'http://forum.raidenftpd.com' + author_url
            dt = textify(node.select('./span/text()').extract()[-1])
            dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
            try:text = textify(node.select('./parent::tr/following-sibling::tr[1]//p[@class="post"]/text()'))
            except:text = textify(node.select('./parent::tr/following-sibling::tr//p[@class="post"]/text()'))
            sk = xcode(title) + comment_id
            import pdb;pdb.set_trace()
'''
            item = Item(response)
            item.set('url',response.url + '#' + comment_id)
            item.set('forum',{'name':xcode(forum_title),'url':forum_url})
            item.set('thread',{'name':xcode(title),'url':response.url,'id':thread_id})
            item.set('title',xcode(title))
            item.set('author',{'name':xcode(author_name),'url':author_url})
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('sk',md5(sk))'''
