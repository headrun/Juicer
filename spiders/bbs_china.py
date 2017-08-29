from juicer.utils import *
from dateutil import parser
import re

class  Bbs_China(JuicerSpider):
    name = "bbs_china"
    start_urls = ['http://bbs.chinanews.com/index.php']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="fl bm"]//div[@class="fl_icn_g"]/a/@href')
        for url in urls:
            yield Request(url,self.parse_forum,response)

    def parse_forum(self,response):

        hdoc = HTML(response)
        threads = hdoc.select('//table[@summary]/tbody[contains(@id,"normalthread")]//th[@class="new"]/a[@onclick]/@href')
        forum_name = textify(hdoc.select('//div[@class="bm_h cl"]/h1/a/text()'))
        forum_id = response.url.split('&')[-1]
        forum_id = forum_id.split('=')[-1]
        forum_url = response.url
        for thread in threads:
            yield Request(thread,self.parse_details,response,meta={"forum_name":forum_name,"forum_id":forum_id,"forum_url":forum_url})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//a[@id="thread_subject"]/text()'))
        text = textify(hdoc.select('//div[1][contains(@id,"post_")]//td[@class="t_f"]//text()[not(ancestor::ignore_js_op)][not(ancestor::span)][not(ancestor::script)]'))
        dt_added = textify(hdoc.select('//em[contains(@id,"poston")]')[0])
        dt_added = dt_added.split(' ')
        try:
            dt_added.pop(0)
            dt_added = dt_added[0]+' '+dt_added[1]
            dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        except:
            dt_added = textify(hdoc.select('//em[contains(@id,"poston")]')[0])
            dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="authi"]/a/text()')[0])

        thread_id = re.findall('t-\d*',response.url)
        thread_id = ''.join(thread_id).replace('t-','')
        if not thread_id:
            thread_id = response.url.split('/')[-1]
            thread_id = thread_id.split('-')[-3]
        forum_name = response.meta['forum_name']
        forum_id = response.meta['forum_id']
        forum_url = response.meta['forum_url']
        print "forum_name:",xcode(forum_name)
        print "forum_id:",xcode(forum_id)
        print "forum_url:",xcode(forum_url)
        print "thread_url:",response.url
        print "thread_id:",xcode(thread_id)
        print "title:",xcode(title)
        print "dt_added:",xcode(dt_added)
        print "author:",xcode(author)
        print "text:",xcode(text)

    #def parse_post_comments(self,response):

        #hdoc = HTML(response)
        #thread_id = response.url.split('/')[-1]
        #thread_id = thread_id.split('-')[-3]
        #forum_name = response.meta['forum_name']
        #forum_id = response.meta['forum_id']
        #forum_url = response.meta['forum_url']
        main = hdoc.select('//div[contains(@id,"post_")][position()>1]')
        for url in main:
            author = textify(url.select('.//td[@class="pls"]//div[@class="pi"]//text()'))
            text = textify(url.select('.//td[@class="t_f"]//text()[not(ancestor::ignore_js_op)]'))
            dt_added = textify(url.select('.//em[contains(@id,"poston")]'))
            dt_added = dt_added.split(' ')
            try:
                dt_added.pop(0)
                dt_added = dt_added[0]+' '+dt_added[1]
                dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
            except:
                dt_added = textify(hdoc('//div[contains(@id,"post_")][position()>1]//em[contains(@id,"poston")]'))
                dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
            #print "forum_name:",xcode(forum_name)
            #print "forum_id:",xcode(forum_id)
            #print "forum_url:",xcode(forum_url)
            print "thread_url:",response.url
            #print "thread_id:",xcode(thread_id)
            print "post_author:",xcode(author)
            print "comment_date:",xcode(dt_added)
            print "post_comment:",xcode(text)
        '''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()
        '''
