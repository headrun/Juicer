from juicer.utils import *

class Pantip(JuicerSpider):
    name = 'pantip_forum_thailand_bak'
    start_urls = ['http://pantip.com/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes =  hdoc.select('//div[@class="submenu-room"]//ul[@class="submenu-room-list"]//li[@class="submenu-room-item"]')
        for node in nodes[:1]:
            node = textify(node.select('.//a//@href'))
            url = 'http://pantip.com' + node
            print url
            forum_id = node.split('/forum/')[-1]
            print "forum_id=",forum_id
            yield Request(url,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        thread = hdoc.select('//div[@class="post-list-wrapper"]//div[@class="post-item-title"]')
        for each_thread in thread[:1]:
            url= textify(each_thread.select('.//a/@href'))
            url ='http://pantip.com/topic/32925237'
            _id = url.split('/topic/')[-1]
            yield Request(url,self.parse_post_details,response)
        next_page = textify(hdoc.select('//div[@class="loadmore-bar indexlist"]/a/@href'))
        url = 'http://pantip.com' + next_page
        #print url
        #yield Request(url,self.parse_next,response)

    def parse_post_details(self,response):
        hdoc = HTML(response)
        false = False
        true = True
        null = ''

        _id = response.url.split('/topic/')[-1]
        cookies = {'__gads':'ID=1bbddc66d9d71bc8:T=1417242447:S=ALNI_Max6t8-y0soUT6-X2hYNXSAMMbToA', '_gat':'1', '_gali':'show_topic_lists', 'rlr':'32918366', 'pantip_visitc':'nfsf9gfxrcIXNMy9R62', '_ga':'GA1.2.2072488316.1417242444'}
        headers ={'Referer': response.url, 'X-Requested-With':'XMLHttpRequest', 'User-Agent':'Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/32.0.1700.107 Chrome/32.0.1700.107 Safari/537.36', 'Accept':'application/json, text/javascript, */*; q=0.01', 'Host':'pantip.com', 'Accept-Encoding':'gzip,deflate,sdch', 'Accept-Language':'en-US,en;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'method':'GET', 'cookie':cookies}

        title = textify(hdoc.select('//h2[@class="display-post-title"]//text()'))
        print "TITLE::::",xcode(title)
        author = textify(hdoc.select('//a[@class="display-post-name owner"]//text()'))
        dt_added = textify(hdoc.select('//span[@class="display-post-timestamp"]//abbr//@data-utime'))
        print "DATE::::",xcode(dt_added)

        if u'\u0e2a\u0e21\u0e32\u0e0a\u0e34\u0e01\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02' in author:
            author = " "
        print "AUTHOR:::::",xcode(author)
        print "THREAD ID:::",_id

        text = textify(hdoc.select('//div[@class="display-post-story"]/text()'))
        print "TEXT:::::::::",xcode(text)
        print "URL::::::",response.url
        print " "
        #_id = response.url.split('/topic/')[-1]

        url = "http://pantip.com/forum/topic/render_comments?tid=%s&param=&type=3" %_id
        yield Request(url,self.parse_post_response, headers=headers)

    def parse_post_response(self,response):
        false = False
        true = True
        null = ''
        data = eval(response.body)
        print comments_list
        for comment in comments_list:
            comment_no = xcode(comment.get('comment_no',''))
            print "comment_ url::::::", url
            comment_id = xcode(comment.get('_id', ''))
            message = xcode(comment.get('message', ''))
            created_time = comment.get('created_time', '')
            user_info = comment.get('user', '')
            if user_info:
                user_name= xcode(user_info.get('name', ''))
                user_ref_url = xcode(user_info.get('link', ''))
                print "comment=======", message
                print "comment_id=========", comment_id
                print "created_time==============", created_time
                print "user_name==========",user_name
                print "user_ref_url========",user_ref_url
                print "Url=============",response.url
                print  "thread_id ===",thread_id


