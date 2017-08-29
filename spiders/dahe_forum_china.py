from juicer.utils import *
from dateutil import parser
import re

class DaheForum(JuicerSpider):
    name = 'dahe_forum_china'
    start_urls = ['http://bbs.dahe.cn/index-htm-m-bbs.htm']
    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="main"]//div[@class="tTable"]//h2')
        for node in nodes:
            node = textify(node.select('.//a//@href'))
            node = 'http://bbs.dahe.cn/' + node
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//tbody[@id="threadlist"]//td[@class="subject"]//a[@name="readlink"]//@href')
        for url in urls:
            forum_id = re.findall('fid-\d*',response.url)[0]
            forum_title= textify(hdoc.select('//h2[@class="mr5 fl f14"]//text()'))
            yield Request(url,self.parse_details,response,meta = {'forum_id':forum_id,'forum_url':response.url,'forum_title':forum_title})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="subject_tpc"]//text()'))
        info = hdoc.select('//div[@class="read_t"]')
        for  inf in info:
            text = textify(inf.select('.//div[@class="tpc_content"]//text()'))
            dt_added = textify(inf.select('.//div[@class="tipTop s6"]//span/text()'))
            author = textify(inf.select('.//div[@class="readName b"]//a//text()'))
            forum_title = response.meta['forum_title']
            forum_id = response.meta['forum_id']
            forum_id = ''.join(forum_id)
            forum_id = forum_id.replace('fid-','')
            forum_url = response.meta['forum_url']
            thread_id = re.findall('tid-\d*',response.url)[0]
            dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

            item = Item(response)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',dt_added)
            item.set('author.name',xcode(author))
            item.set('thread.id',thread_id)
            item.set('forum.id',forum_id)
            item.set('forum.title',forum_title)
            item.set('forum.url',forum_url)
            item.set('thread.url',response.url)
            yield item.process()
