from juicer.utils import *
from dateutil import parser

class RenotalkForum(JuicerSpider):
    name = 'renotalk_forum'
    start_urls = 'http://www.renotalk.com/forum/'

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//td[@class="col_c_forum"]/h4/a/@href').extract()

        for link in links:
            yield Request(link,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        forum_title = textify(hdoc.select('//h1[@class="ipsType_pagetitle"]/text()'))
        forum_id = response.url.split('forum/')[-1].split('-')[0]
        forum = {'name':xcode(forum_title),'id':forum_id,'url':response.url}
        last_postlinks = hdoc.select('//ul[@class="last_post ipsType_small"]//a[contains(@title,"Go to last post")]')

        for last_postlink in last_postlinks:
            date = textify(last_postlink.select('./text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                continue
            thread_links = textify(last_postlink.select('./@href'))
            yield Request(thread_links,self.parse_details,response,meta={'forum':forum})

        next_page = hdoc.select('//li[@class="next"]/a[@title="Next page"]/@href').extract()
        if next_page:
            next_page = next_page[0]
            yield Request(next_page,self.parse_next,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        is_next = True
        title = textify(hdoc.select('//h1[@class="ipsType_pagetitle"]/text()'))
        thread_id = response.url.split('topic/')[-1].split('-')[0]
        nodes = hdoc.select('//div[contains(@id,"post_id_")]')

        for node in nodes:
            author_name = textify(node.select('.//span[@class="author vcard"]/text()'))
            dt = textify(node.select('.//p/abbr[@class="published"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
            text = textify(node.select('.//div[@class="post entry-content "]//text()'))
            comment_url = textify(node.select('.//a[@itemprop="replyToUrl"]/@href'))
            other_info = textify(node.select('.//ul[@class="basic_info"]//text()'))
            sk = comment_url

            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            item = Item(resposne)
            item.set('url',comment_url)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('auhtor',{'name':xcode(author_name),'other_info':xcode(other_info)})
            item.set('forum',response.meta['forum'])
            item.set('thread',{'name':xcode(title),'id':thread_id,'url':response.url})
            item.set('xtags',['forums_sourcetype_manual','singapore_country_manual'])
            item.set('sk',md5(sk))
            yield item.process()

        nxt_page = hdoc.select('//li[@rel="next"]/a/@href').extract()
        if nxt_page and is_next:
            nxt_page = nxt_page[0]
            yield Request(nxt_page,self.parse_details,response,meta={'forum':response.meta['forum']})
