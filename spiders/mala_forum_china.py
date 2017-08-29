from juicer.utils import *
from dateutil import parser
import re

class MalaForum(JuicerSpider):
    name = 'mala_forum_china'
    start_urls = ['http://bbs.mala.cn/']
    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="bm bmw  flg cl"]//td[@class="fl_g"]//dt')
        for node in nodes[:1]:
            node = textify(node.select('.//a//@href'))
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        forum_title = textify(hdoc.select('//div[@class="z"]//a[contains(@href , ".html")]//text()'))
        urls = hdoc.select('//th[@class="new"]//a[contains(@href , "mala.cn/thread")]//@href')
        for url in urls[:1]:
            url = textify(url)
            url = 'http://bbs.mala.cn/thread-11599384-1-1.html'
            forum_id = re.findall('forum-\d*',response.url)[0]
            yield Request(url,self.parse_details,response,meta = {'forum_id':forum_id ,'forum_url':response.url ,'forum_title':forum_title})


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="ts"]//span[@id="thread_subject"]//text()'))
        #import pdb;pdb.set_trace()
        info = hdoc.select('//div[@id="postlist"]//td[@class="plc"]')
        for inf in info:
            text = textify(inf.select('.//div[@class="t_fsz"]//td[@class="t_f"]//text()'))
            author =textify(hdoc.select('.//div[@class="pi"]//div[@class="authi"]//a//text()'))
            dt_added = textify(inf.select('.//div[@class="pti"]//div[@class="authi"]//em[contains(@id , "authorposton")]//text()'))

            thread_id = textify(hdoc.select('//h1[@class="ts"]//span/a/@href'))
            thread_id = re.findall('thread-\d*',thread_id)[0]
            thread_id = thread_id.replace('thread-','')
            forum_id = response.meta['forum_id']
            forum_id = forum_id.replace('forum-','')
            forum_url = response.meta['forum_url']
            forum_title = response.meta['forum_title']
            print "title:",xcode(title)
            print "text:",xcode(text)
            print "date:",xcode(dt_added)
            print "thread_id =",thread_id
            print "forum_name::",xcode(forum_title)
            print "forum_id=" ,forum_id
            print "forum_url=",forum_url
            print "thread_url=",response.url
        '''
        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('thread.id',thread_id)
        item.set('forum.id',forum_id)
        item.set('forum.title',forum_title)
        item.set('forum.url',forum_url)
        item.set('thread.url',response.url)
        #yield item.process()
        '''
