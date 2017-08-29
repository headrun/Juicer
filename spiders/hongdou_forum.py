from juicer.utils import *
from dateutil import parser

class  Hongdou(JuicerSpider):
    name = "hongdou_forum"
    start_urls = ['http://hongdou.gxnews.com.cn/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td[@valign="middle"]/span[@class="style15"]/a[contains(@href,"viewforum")]/@href' and '//td[@onmouseover]/div/a[contains(@href,"viewforum")]/@href')
        #urls = hdoc.select('//td[@onmouseover]')
        #forum_name = textify(hdoc.select('//td[@onmouseover]/div/a/text()'))
        for url in urls:
            #url = url.select('./div/a[contains(@href,"viewforum")]/@href')
            #forum_name = textify(url.select('./div/a/text()'))
            #print url,forum_name
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        threads = hdoc.select('//div[@id="nomalThread"]/div[@class="threadbit1"]/div[1]/a[contains(@href,"viewthread")]/@href').extract()
        forum_id = response.url.split('-')[1]
        forum_id = forum_id.strip('.html')
        forum_name = textify(hdoc.select('//div[@id="bbsnavbar"]/div[1]/span[2]/a/text()'))
        forum_url = response.url
        for thread in threads:
            if "http:" not in thread:
                thread = 'http://hongdou.gxnews.com.cn/'+thread

            yield Request(thread,self.parse_thread,response,meta={'forum_name':forum_name,'forum_id':forum_id,'forum_url':forum_url})

    def parse_thread(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="postbit"][1]/table[@class="posttable"]//div[@class="thead"]/text()'))
        title = title.split(':')
        title = title[1]
        text = textify(hdoc.select('//div[@class="postbit"][1]/table[@class="posttable"]/tr[2]/td[@class="alt1"]//div[3]//text()'))
        dt_added = textify(hdoc.select('//div[@class="postbit"][1]/table[@class="posttable"]/tr[2]/td[@class="alt1"]//td[5]/text()')[2])
        dt_added = dt_added.strip(u'\u7b2c')
        dt_added = "".join(dt_added)
        #import pdb;pdb.set_trace()
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="postbit"][1]/table[@class="posttable"]/tr[2]/td[@class="alt2"]//div[3]/a//text()'))
        forum_name = response.meta['forum_name']
        forum_id = response.meta['forum_id']
        forum_url = response.meta['forum_url']
        thread_id = response.url.split('-')[-1]
        thread_id= thread_id.split('.')[0]
        print "title:",title
        print "forum_name :",forum_name
        print "forum_id :",forum_id
        print "forum_url:",forum_url
        print "thread_id :",thread_id
        print "thread_url:",response.url
        print "author:",author
        print "date :",dt_added
        print "text :",text

        #dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

    #def parse_post_comments(self,response):
       # hdoc = HTML(response)
        try:
            urls = hdoc.select('//div[@class="postbit"][position()>1]/table[@class="posttable"]')
        except:
            urls = ''
        #post_date = post_date.strip(u'\u7b2c')
        #forum_name = response.meta['forum_name']
        #forum_id = response.meta['forum_id']
        #forum_url = response.meta['forum_url']
        #thread_id = response.url.split('-')[-1]
        #thread_id= thread_id.split('.')[0]
        for url in urls:
            dt_added = textify(url.select('.//td[@class="alt1"]//td[4]/text()'))
            dt_added = dt_added.split(' ')
            dt_added = dt_added[1]+" "+dt_added[2]
            dt_added = dt_added.strip(u'\u7b2c')
            dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
            author = textify(url.select('.//td[@class="alt2"]//div[3]/a//text()'))
            text = textify(url.select('.//td[@class="alt1"]//div[1]//text()'))
            text = text.replace('-','')
            #print "forum_name :",forum_name
            #print "forum_id :",forum_id
            #print "forum_url:",forum_url
            #print "thread_id :",thread_id
            print "thread_url:",response.url
            print "comment_author:",author
            print "comment_date :",dt_added
            print "comment_text :",text
            print "\n"
        '''
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()
        '''
