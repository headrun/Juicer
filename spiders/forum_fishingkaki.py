from juicer.utils import*
from dateutil import parser
import re
class Fishingkaki(JuicerSpider):
    name = 'forum_fishingkaki'
    start_urls = ['http://forum.fishingkaki.com/categories']


    def parse(self,response):
        hdoc = HTML(response)
        nodes_categories = hdoc.select('//div[@class="ItemContent Category"]')
        for category in nodes_categories[:2]:
            date = textify(category.select('.//span[@class="MItem LastCommentDate"]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                continue
            sub_category = textify(category.select('.//div[@class="TitleWrap"]/a/@href'))
            yield Request(sub_category,self.parse_threads,response)

    def parse_threads(self,response):
        hdoc = HTML(response)
        is_next = True
        sub_title = textify(hdoc.select('//h1[@class="H HomepageTitle"]/text()'))
        forum = {'url':response.url,'title':sub_title}
        nodes = hdoc.select('//div[@class="ItemContent Discussion"]')
        for node in nodes:
            thread_date = textify(node.select('.//span[@class="MItem LastCommentDate"]/time/text()'))
            date_added = get_timestamp(parse_date(xcode(thread_date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            thread_link = textify(node.select('./div[@class="Title"]/a/@href'))
            yield Request(thread_link,self.parse_data,response,meta={'forum':forum})

        next_pg = textify(hdoc.select('//div[@id="PagerAfter"]//a[@class="Next"]/@href'))
        if next_pg and is_next:
            yield Request(next_pg,self.parse_threads,response)

    def parse_data(self,response):
        hdoc = HTML(response)
        is_next = True
        forum = response.meta['forum']
        post_title = textify(hdoc.select('//h1[@class="H"]/text()'))
        import pdb;pdb.set_trace()
        post_id =textify(re.findall('(\d+)/',response.url))
        thread = {'url':response.url,'title':post_title,'id':post_id}
        posts = hdoc.select('//div[@class="Item-Body"]')
        for post in posts:
            comment_date = textify(post.select('.//span[@class="MItem DateCreated"]//time/text()'))
            comment_author = textify(post.select('.//span[@class="AuthorName"]/a[@class="Username"]/text()'))
            author_link = textify(post.select('.//span[@class="AuthorName"]/a[@class="Username"]/@href'))
            if 'http' not in author_link: author_link = 'http://forum.fishingkaki.com' + author_link
            _author = {'name':comment_author,'url':author_link}
            comment_text = textify(post.select('.//div[@class="Message"]//text()')) or textify(post.select('.//div[@class="Message"]//div/text()'))
            comment_url = textify(post.select('.//span[@class="MItem DateCreated"]/a/@href'))
            if 'http' not in comment_url: comment_url = 'http://forum.fishingkaki.com' + comment_url
            dt_added = get_timestamp(parse_date(xcode(comment_date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
        next_pg = textify(hdoc.select('//div[@id="PagerAfter"]//a[@class="Next"]/@href'))
        if next_pg and is_next:
            yield Request(next_pg,self.parse_data,response,meta={'forum':forum})
        print forum
        print thread
        print comment_url
        print 'title',xcode(post_title)
        print 'text',xcode(comment_text)
        print 'dt_added',xcode(dt_added)
        import pdb;pdb.set_trace()
'''
            sk = comment_url
            item = Item(response)
            item.set('url',comment_url)
            item.set('title',post_title)
            item.set('text',comment_text)
            item.set('dt_added',comment_date)
            item.set('forum',forum)
            item.set('thread',thread)
            item.set('sk',md5(sk))
        next_pg = textify(hdoc.select('//div[@id="PagerAfter"]//a[@class="Next"]/@href'))
        if next_pg and is_next:
            yield Request(next_pg,self.parse_data,response,meta={'forum':forum})'''
