
from juicer.utils import *
from dateutil import parser

class  TiebaBaidu(JuicerSpider):
    name = "tieba_baidu"
    start_urls = ['http://tieba.baidu.com/f?kw=%CB%D1%B9%B7%CB%B5%B0%C9']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="forum_content clearfix"]//ul[@id="thread_list"]/li[contains(@class,"j_thread_list clearfix")]//a[@class="j_th_tit"]/@href').extract()
        for url in urls:
            if "http:" not in url:
                url = 'http://tieba.baidu.com'+url
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="pb_content"]//div[@id="j_core_title_wrap"]//h1/text()'))
        text = textify(hdoc.select('//div[@class="d_post_content_main d_post_content_firstfloor"]//div[@class="d_post_content j_d_post_content "]//text()'))
        dt_added = textify(hdoc.select('//div[@class="d_post_content_main d_post_content_firstfloor"]//div[@class="core_reply j_lzl_wrapper"]//span[@class="j_reply_data"]/text()'))
        author = textify(hdoc.select('//div[@class="d_author"]//li[@class="d_name"]//text()')[1])
        thread_id = response.url.split('/')[-1]
        #dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        print "title :",xcode(title)
        print "author :",xcode(author)
        print "Date :",xcode(dt_added)
        print "Thread id:",xcode(thread_id)
        print "Thread_url:",response.url
        print "text :",xcode(text)
        '''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()
        '''

