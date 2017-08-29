from juicer.utils import *
from dateutil import parser
import re

class KdnetForum(JuicerSpider):
    name = 'kdnet_forum_china'
    start_urls = ['http://www.kdnet.net/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="content"]//div[@class="gb-t"]')
        for node in nodes[:1]:
            node = textify(node.select('.//a[contains(@href , "kdnet.net/lists.asp?")]//@href'))
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc =HTML(response)
        forum_name = re.findall('name=.*',response.url)
        forum_name = forum_name[0]
        forum_name = forum_name.replace('name=','')
        forum_id = re.findall('id=\d+',response.url)
        forum_id = forum_id[0]
        forum_id = forum_id.replace('id=','')
        urls = hdoc.select('//ul[@class="c-main glist-l40 article-list"]//li//a//@href')
        for url in urls[:1]:
            yield Request(url,self.parse_details,response,meta={'forum_id' :forum_id , 'url' :response.url,'name':forum_name})

    def generate_item(self, title, text, dt_added, thread, forum, response):
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('author', author)
        item.set('url', url)
        item.set('forum', forum)
        item.set('thread', thread)

        return item

    def parse_details(self,response):
        hdoc = HTML(response)
        forum_id = response.meta['forum_id']
        forum_url = response.meta['url']
        forum_title = response.meta['name']
        forum = {'forum.title':forum_title ,'forum.url':forum_url,'forum.id':forum_id}
        title = textify(hdoc.select('//div[@class="posts-title"]//text()'))
        text = textify(hdoc.select('//div[@class="posts-cont "]//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="posts-cont"]//text()'))
        dt_added = textify(hdoc.select('//div[@class="posts-posted"]/text()'))
        if dt_added:
            dt_added = dt_added.split(' ')
            dt_added.pop(0)
            dt_added.pop(-1)
            dt_added = ' '.join(dt_added)
        thread_id = re.findall('tid=\d*',response.url)
        thread = {'thread.title':title,'thread.id':thread_id , 'thread.url':response.url}
        item = self.generate_item(title, text, dt_added, thread, forum, response)
        yield item.process()

        comments = hdoc.select('//div[contains(@class , "reply-box")]')
        for cmnt in comments:
            text = textify(cmnt.select('.//div[@class="replycont-text"]//text()'))
            dt_added = textify(cmnt.select('.//div[@class="posted-info c-sub"]/text()'))
            dt_added = re.findall('\d*-\d*-\d* \d*:\d*:\d*',dt_added)[0]
            item = self.generate_item(title, text, dt_added, response.meta['thread'], response.meta['forum'], response)
            yield item.process()
