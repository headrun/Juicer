from juicer.utils import *
from dateutil import parser
import re

class Scol(JuicerSpider):

    name = 'scol'
    start_urls = ['http://www.scol.cn/forum.php']

    def parse(self,response):

        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="sub-nav"]//div[not(contains(@class,"sub-nav1"))]')
        for node in nodes:
            node = node.select('./a[not(contains(@class,"strike"))]/@href')
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):

        hdoc = HTML(response)
        forum_id = response.url.split('/')[-1]
        forum_id = forum_id.strip('.html')
        for_id = forum_id.split('-')
        for_id.pop(0)
        forum_id = for_id[0]
        forums = hdoc.select('//div[@id="threadlist"]//table/tbody[contains(@id,"thread")]//th[@class="new"]/a[1]/@href')
        forum_name = textify(hdoc.select('//div[@class="bm_h cl"]//h1/a/text()'))
        forum_url = response.url
        for forum in forums:
            yield Request(forum,self.parse_details,response,meta={"forum_id":forum_id,"forum_name":forum_name,"forum_url":forum_url})

    def parse_details(self,response):

        hdoc = HTML(response)
        dt_added = textify(hdoc.select('//div[@class="wp cl"]//div[@id="postlist"]/div[1]//td[@class="floor-plc"]//p[@class="cp_pls"]/em/text()'))
        dt_added = dt_added.split(' ')
        dt_added = dt_added[1]+' '+dt_added[2]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        '''try:
            dt = re.findall('.*(\d{4}).*(\d{2}).*(\d{2}).*\s(\d{2}:\d{2})',dt_added)
            dt_added = dt[0][0]+'-'+dt[0][1]+'-'+dt[0][2]+" "+dt[0][3]
        except:
            try:
                dt = re.findall(".*(\d{4}).*(\d{1}).*(\d{2}).*\s(\d{2}:\d{2})",dt_added)
                dt_added = dt[0][0]+'-'+dt[0][1]+'-'+dt[0][2]+" "+dt[0][3]
            except:
                dt = re.findall(".*(\d{4}).*(\d{1}).*(\d{1}).*\s(\d{2}:\d{2})",dt_added)
                dt_added = dt[0][0]+'-'+dt[0][1]+'-'+dt[0][2]+" "+dt[0][3]'''

        author = textify(hdoc.select('//div[@class="wp cl"]//div[@id="postlist"]/div[1]//div[@class="floor-top cl"]/div[@class="pti cl"]/div[@class="authi"]/div[@class="floor-profile"]/a[1]/text()'))
        title = textify(hdoc.select('//div[@class="thread-title"]/h1/a/text()'))
        text = textify(hdoc.select('//div[@id="postlist"]/div[1]//div[@class="pct"]/div[@class="pcb"]//td[@class="t_f"]//text()[not(ancestor::ignore_js_op)]'))
        forum_id = response.meta['forum_id']
        forum_name = response.meta['forum_name']
        forum_url = response.meta['forum_url']
        thread_url = response.url
        thread_id = thread_url.split('/')[-1]
        thread_id = thread_id.strip('.html')
        thread_id = thread_id.split('-')
        thread_id.pop(0)
        thread_id = thread_id[0]

        print "forum_name :",xcode(forum_name)
        print "forum_id   :",xcode(forum_id)
        print "forum_url  :",xcode(forum_url)
        print "title      :",xcode(title)
        print "author     :",xcode(author)
        print "thread_id  :",xcode(thread_id)
        print "thread_url :",xcode(thread_url)
        print "date       :",xcode(dt_added)
        print "text       :",xcode(text)

    #def parse_post_comments(self,response):

        #hdoc = HTML(response)
        main_post = hdoc.select('//div[@id="postlist"]/div[@class="floor"][position()>1]/table/tr[2]//div[@class="authi"]')
        #forum_id = response.meta['forum_id']
        #forum_name = response.meta['forum_name']
        #forum_url = response.meta['forum_url']
        #thread_url = response.url
        for post in main_post:
            post_author = textify(post.select('./div[@class="floor-profile"]/a[1]'))
            post_date = textify(post.select('./p[@class="cp_pls"]/em/text()'))
            post_date = post_date.split(' ')
            post_date.pop(0)
            post_date = post_date[0]+' '+post_date[1]
            post_date = get_timestamp(parse_date(xcode(post_date)) - datetime.timedelta(hours=8))
            post_comment = textify(post.select('//div[@id="postlist"]/div[@class="floor"][position()>1]/table/tr[2]//div[@class="pct"]//td[@class="t_f"]//text()[not(ancestor::ignore_js_op)]'))
            print "forum_name :",xcode(forum_name)
            print "forum_id   :",xcode(forum_id)
            print "forum_url  :",xcode(forum_url)
            print "thread_url :",xcode(thread_url)
            print "post_author :",xcode(post_author)
            print "post_date   :",xcode(post_date)
            print "post_comment:",xcode(post_comment)
            print "\n"

