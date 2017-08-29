from juicer.utils import *
from dateutil import parser
import re

class PeopleForum(JuicerSpider):
    name = "people_forum_china"
    start_urls = ['http://bbs1.people.com.cn/']
    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="p2_content p-g clearfix"]//h4[@class="clearfix"]')
        for node in nodes:
            f_title = textify(node.select('.//a//text()'))
            node = textify(node.select('.//a//@href'))
            yield Request(node,self.parse_next,response, meta= {'f_title':f_title})

    def parse_next(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//ul//li//a[@class="treeReply"]')
        for url in urls:
            term_url = textify(url.select('.//@href'))
            title = textify(url.select('.//text()'))
            forum_id = ''.join((response.url).split('/board/')[-1])
            forum_id = forum_id.split('_')[0]
            if 'html' in forum_id:
                forum_id = forum_id.split('.html')[0]
            yield Request(term_url,self.parse_details,response ,meta = {'title':title , 'forum_id':forum_id,'forum_url':response.url ,'f_title':response.meta['f_title']})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="artibodyTitle"]//text()'))
        if not title:
            title = response.meta['title']
        text =textify(hdoc.select('//div[@id="artibody"]//text()'))
        if not text:
            text = textify(hdoc.select('//p//text()'))
        dt_added =textify(hdoc.select('//span[@id="pub_date"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//div//text()'))
            dt_added = re.findall('\d*-\d*-\d* \d*:\d*:\d*',dt_added)[0]
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        forum_id = response.meta['forum_id']
        forum_url = response.meta['forum_url']
        thread_id = re.findall('\d*.html',response.url)[-1].split('.html')[0]
        forum_title = response.meta['f_title']

        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('thread.id',thread_id)
        item.set('forum.id',forum_id)
        item.set('forum.title',forum_title)
        item.set('forum.url',forum_url)
        item.set('thread.url',response.url)
        yield item.process()
