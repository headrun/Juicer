from juicer.utils import *
from dateutil import parser
import re

class Koubei(JuicerSpider):
    name = 'koubei'
    start_urls = ['http://bbs.taobao.com/']
    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="nav"]//div[@class="more-nav"]//div//dl//dd')
        for node in nodes:
            node = textify(node.select('./a[not(contains(@href,"index"))]/@href'))
            yield Request(node,self.parse_next)

    def parse_next(self,response):
        hdoc = HTML(response)
        forums =  hdoc.select('//div[@id="content"]/div[@class="grid-c2"]//div[@class="bd"]/table[@class="posts"]//tr//div[@class="detail"]/a/@href|//div[@class="xx_content"]//ul[@class="chanpin clearfix"]//li//a/@href')
        forum_id = response.url.split('/')
        forum_id = forum_id[4]
        forum_id = forum_id.split('.')[0]
        forum_url = response.url
        forum_name = hdoc.select('//div[@id="nav"]//div[@class="more-nav"]//div//dl//dd/a[not(contains(@href,"index"))]//text()')
        for forum in forums[:1]:
            yield Request(forum,self.parse_detail,meta={'forum_id':forum_id,'forum_url':forum_url})

    def parse_detail(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="detail-title"]/h4'))
        dt_added = textify(hdoc.select('//div[@class="detail-post first"]/div[@id="reply0"]/div[@class="floor-wrap"]/div[@class="hd"]/span[1]/text()'))
        dt = re.findall('.*(\d{4}).*(\d{2}).*(\d{2}).*\s(\d{2}\:\d{2})',dt_added)
        try:
            dt_added = dt[0][0]+'-'+dt[0][1]+'-'+dt[0][2]+" "+dt[0][3]
            dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        except:
            try:
                dt_added = textify(hdoc.select('//div[@class="detail-post first"]/div[@id="reply0"]/div[@class="floor-wrap"]/div[@class="hd"]/span[1]/text()'))
                dt_added = dt_added.split(' ')
                dt_added = dt_added[1]
                dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
            except:
                dt_added = ''
        '''text = textify(hdoc.select('//div[@class="bbd"]//div[@id="reply0"]/div[@class="floor-wrap"]//div[@class="bd"]/div[@class="article"]//div[@class="ke-post"]//p//text()|//div[@class="bbd"]//div[@id="reply0"]/div[@class="floor-wrap"]//div[@class="bd"]/div[@class="article"]//div[@class="ke-post"]/div//text()'))'''
        text = textify(hdoc.select('//div[@class="floor one"]//div[@class="article"]//div[@class="ke-post"]//text()|//div[@class="floor one"]//div[@class="article"]//div[@class="ke-post"]/div//text()'))
        text = text.replace('-','')
        author = textify(hdoc.select('//div[@class="floor one"]/following-sibling::div//h4//text()'))
        forum_id = response.meta["forum_id"]
        forum_url = response.meta["forum_url"]
        forum_name = textify(hdoc.select('//div[@id="content"]/div[@id="crumb"]/a[2]/text()'))
        thread_id = re.findall('\d+',response.url)
        thread_id = thread_id[0]+'-'+thread_id[1]
        print "title :",xcode(title)
        print "Date :",xcode(dt_added)
        print "author:",xcode(author)
        print "forum_id:",xcode(forum_id)
        print "forum_name:",xcode(forum_name)
        print "thread_id:",xcode(thread_id)
        print "thread_url:",response.url
        print "text:",xcode(text)
        #yield Request(response.url,self.parse_post_comments,response)

    #def parse_post_comments(self,response):
        #hdoc = HTML(response)
        #import pdb;pdb.set_trace()

        posts = hdoc.select('//div[@class="bbd"]/div[@class="detail-post"]')
        for post in posts:
            post_date = textify(post.select('.//span[@class="time-author"]/text()'))
            try:
                #dt = re.findall('.*(\d{4}).*(\d{2}).*(\d{2}).*\s(\d{2}\:\d{2})',post_date)
                #post_date = dt[0][0]+'-'+dt[0][1]+'-'+dt[0][2]+" "+dt[0][3]
                post_date = post_date.split(' ' )
                dt_added = post_date[1]+' '+post_date[2]
                post_date = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
            except:
                post_date = textify(post.select('.//span[@class="time-author"]/text()'))
                pt = post_date.split(' ')
                post_date = pt[1]
            post_author = textify(post.select('./div[@class="floor"]/following-sibling::div//h4//text()'))
            post_content = textify(post.select('.//div[@class="bd"]//div[@class="ke-post"]//text()'))
            #forum_id = response.meta["forum_id"]
            #forum_url = response.meta["forum_url"]
            #import pdb;pdb.set_trace()
            print "forum_id :",xcode(forum_id)
            print "forum_url :",xcode(forum_url)
            print "comment_date :",xcode(post_date)
            print "comment_author:",xcode(post_author)
            print "comment_text :",xcode(post_content)
            print "thread_url:",response.url
            print '\n'


