from juicer.utils import *
from dateutil import parser


class QqForum(JuicerSpider):

    name = 'qqforum'
    start_urls = ['http://bbs.news.qq.com/forum.php','http://bbs.ent.qq.com/forum.php','http://bbs.sports.qq.com/forum.php','http://club.auto.qq.com/forum.php']


    def parse(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="fl bm"]//div[2]//td[@class="fl_icn"]/a/@href')
        forum_name = textify(hdoc.select('//div[@class="bm_h cl"]/h2/a/text()')[0])
        url= response.url
        #import pdb;pdb.set_trace() 
        for node in nodes[:1]:
            if "news" in url:
                node = 'http://bbs.news.qq.com/' + textify(node)
            elif "ent" in url:
                node = 'http://bbs.ent.qq.com/' + textify(node)
            elif "auto" in url:
                node = 'http://bbs.club.auto.qq.com/' + textify(node)
            else:
                node = 'http://bbs.sports.qq.com/' + textify(node)
            yield Request(node,self.parse_next,response,meta={"forum_name":forum_name})

    def parse_next(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="bm_c"]//tbody[contains(@id,"thread")]//a[@class="xst"]/@href')
        forum_url = response.url
        for url in urls:
            if "news" in forum_url:
                url = 'http://bbs.news.qq.com/' + textify(url)
            elif "ent" in forum_url:
                url = 'http://bbs.ent.qq.com/' + textify(url)
            elif "auto" in forum_url:
                url = 'http://bbs.auto.qq.com/'+textify(url)
            else:
                url = 'http://bbs.sports.qq.com/'+textify(url)

            forum_id = re.findall('f-\d*',response.url)
            forum_id = ''.join(forum_id).replace('f-','')
            forum_name = response.meta['forum_name']
            yield Request(url,self.parse_details,response,meta={"forum_id":forum_id,"forum_url":forum_url,"forum_name":forum_name})

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="ts"]/a[contains(@id,"thread_subject")]/text()'))
        text = textify(hdoc.select('//div[@id][1]//td[contains(@id,"postmessage")]//text()[not(ancestor::ignore_js_op)]'))
        author = textify(hdoc.select('//div[@id][1]//div[@class="pi"]/div[@class="authi"]/a[1]/text()'))
        dt_added = textify(hdoc.select('//div[@id][1]//div[@class="authi"]//em/text()'))

        dt_added = dt_added.split(' ')
        try:
            dt_added = dt_added[1]+' '+dt_added[2]
            dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        except:
            dt_added = textify(hdoc.select('//div[@id][1]//div[@class="authi"]//em//text()'))
        thread_id = re.findall('t-\d*',response.url)
        thread_id = ''.join(thread_id).replace('t-','')
        forum_id = response.meta['forum_id']
        forum_url = response.meta['forum_url']
        forum_name = response.meta['forum_name']

        print "forum_id :",xcode(forum_id)
        print "forum_name:",xcode(forum_name)
        print "forum_url:",xcode(forum_url)
        print "thread_url:",response.url
        print "thread_id:",thread_id
        print "title:",xcode(title)
        print "author:",xcode(author)
        print "date:",xcode(dt_added)
        print "text   :",xcode(text)
        print "\n"

    #def parse_post_comments(self,response):
        #print "In Parse Post Comments Function"

        #hdoc = HTML(response)
        main = hdoc.select('//div[contains(@id,"post_")][position()>1]')
        #forum_id = response.meta['forum_id']
        #forum_url = response.meta['forum_url']
        for url in main:
            author = textify(url.select('.//div[@class="pi"]/div[@class="authi"]/a[1]/text()'))
            dt_added = textify(url.select('.//div[@class="authi"]//em/text()'))
            dt_added = dt_added.split(' ')
            try:
                dt_added = dt_added[1]+' '+dt_added[2]
                dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
            except:
                dt_added = textify(url.select('.//div[@class="authi"]//em//text()'))

            text = textify(url.select('.//td[contains(@id,"postmessage")]//text()[not(ancestor::ignore_js_op)]'))
            print "thread_url :",xcode(response.url)
            print "post_author :",xcode(author)
            print "dt_added :",xcode(dt_added)
            print "text :",xcode(text)
