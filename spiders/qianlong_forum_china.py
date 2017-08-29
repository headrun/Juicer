from juicer.utils import *
from dateutil import parser

class QianlongForum(JuicerSpider):
    name = 'qianlong_forum_china'
    start_urls = ['http://bbs.qianlong.com/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="mn"]//div[@class="bm bmw  flg cl"]//td[@class="fl_g"]//div[@class="fl_icn_g"]')
        for node in nodes:
            node = textify(node.select('.//a//@href'))
            node = 'http://bbs.qianlong.com/' + node
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        sub_nodes = hdoc.select('//div[contains(@id , "subforum")]//tr//td//h2//a//@href')
        if sub_nodes:
            for sub_node in sub_nodes:
                sub_node = 'http://bbs.qianlong.com/' + textify(sub_node)
                yield Request(sub_node,self.parse_subnode_urls,response)
        else:
            yield Request(response.url,self.parse_subnode_urls,response)

    def parse_subnode_urls(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="bm_c"]//tbody[contains(@id , "normalthread")]')
        for ur in urls[:1]:
            url = textify(ur.select('.//th[@class="new"]//a[@class="xst"]//@href'))
            author = textify(ur.select('.//td[@class="by"]//cite//a//text()'))
            url = 'http://bbs.qianlong.com/' + textify(url)
            forum_id = ''.join(re.findall('-\d*-',response.url)).replace('-','').strip()
            yield Request(url,self.parse_details,response,meta = {'forum_id':forum_id , 'forum_url':response.url , 'author':author})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="ts"]//text()')).strip()
        dt_added = textify(hdoc.select('//div[@class="wp cl"]//div[@id="postlist"]/div[1]//td[@class="plc"]//div[@class="authi"]/em/text()'))
        text = textify(hdoc.select('//div[@id="postlist"]//div[1]//div[@class="pct"]//div[@class="pcb"]//div[@class="t_fsz"]//td[@class="t_f"]//text()'))
        author = response.meta['author']
        forum_id = response.meta['forum_id']
        forum_url = response.meta['forum_url']
        thread_id = ''.join(re.findall('thread-\d*-',response.url)).replace('-' ,'').strip()
        thread_id = thread_id.replace('thread','').strip()
        print "thread_id: ",thread_id
        print "forum_id:: ",forum_id
        print "forum_url: ",forum_url
        print "title::::: ",xcode(title)
        print "text:::::: ",xcode(text)
        print "date:::::: ",xcode(dt_added)
        print "author::: ",xcode(author)
        print "thread_url:",response.url
        item = Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('thread.id',thread_id)
        item.set('forum.id',forum_id)
        #item.set('forum.title',forum_title)
        item.set('forum.url',forum_url)
        item.set('thread.url',response.url)
        #yield item.process()

