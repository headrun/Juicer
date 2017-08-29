from juicer.utils import *

class  Lowyat(JuicerSpider):
    name = "lowyat"
    start_urls = ['https://forum.lowyat.net/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="borderwrap"]//td[@class="row2"]/b/a/@href').extract()
        for url in urls[:2]:
            if "https:" not in url:
                url = "https://forum.lowyat.net"+url
                yield Request(url,self.parse_forum,response)

    def parse_forum(self,response):
        hdoc = HTML(response)
        forums = hdoc.select('//div[@id="forum_topic_list"]//tr')
        is_next = True
        for forum in forums:
            forum_url = textify(forum.select('.//div[@class="topic_title"]/span[contains(@class,"minipagelink")][last()]/a/@href'))
            last_action = textify(forum.select('./td[@class="row2"]/span[@class="lastaction"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(last_action)) - datetime.timedelta(hours=8))
            if last_action and dt_added < get_current_timestamp()-86400*60:
                is_next = False
                continue
            if not forum_url: forum_url = textify(forum.select('.//div[@class="topic_title"]/a[1]/@href'))
            if not forum_url: forum_url = textify(forum.select('./td[@class="row1"]//div[@style="float:left"]/a[1]/@href'))
            if  forum_url and "https:" not in forum_url:
                url = 'https://forum.lowyat.net'+forum_url
                import pdb;pdb.set_trace()
                url = 'https://forum.lowyat.net/topic/3603223/+1500'
                yield Request(url,self.parse_thread,response,meta = {'forum_url':url})

        next_page = hdoc.select('//td[@nowrap="nowrap"]/span[@class="pagelink"]/a[@title="Next page"]/@href')
        if next_page and 'http:' not in next_page and is_next:
            url = 'https://forum.lowyat.net'+textify(next_page)
            #yield Request(next_page,self.parse_forum,response)

        sub_forums = hdoc.select('//div[@class="borderwrap"]//td[@class="row2"]/b/a[not(contains(@href,"https:"))]/@href').extract()
        if sub_forums:
            for sub_forum in sub_forums:
                if "http:" not in sub_forum:
                    url = 'https://forum.lowyat.net'+sub_forum
                    #yield Request(url,self.parse_forum,response)

    def parse_thread(self,response):
        hdoc = HTML(response)
        forum_title = textify(hdoc.select('//div[@id="navstrip"]/a[last()]/text()'))
        forum_url = textify(hdoc.select('//div[@id="navstrip"]/a[last()]/@href'))
        forum_id = forum_url.split('/')[-1]
        is_next = True
        if 'http:' not in forum_url:
            forum_url = 'https://forum.lowyat.net'+textify(forum_url)
        forum = {'title':forum_title,'url':forum_url}
        thread_id = response.url.split('/')[-1]
        if '+' in thread_id:
            thread_id = response.url.split('/')[-2]
        title = textify(hdoc.select('//div[@id="topic_content"]/div[@class="maintitle"]/p/b//text()'))
        posts = hdoc.select('//table[@class="post_table"]')
        thread = {'title':title,'id':thread_id,'url':response.url}
        for post in posts:
            text = textify(post.select('.//div[@class="postcolor post_text"]//text()'))
            dt_added = textify(post.select('.//div[@style="float: left;"]/span[@class="postdetails"]//text()'))
            try:
                dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
            except:
                dt_added = dt_added.split(',')
                dt_added.pop(-1)
                dt_added = "".join(dt_added)
                dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*60:
                is_next = False
                continue
            post_id = textify(post.select('.//div[@class="postcolor post_text"]/@data-postid'))
            url = 'http://forum.lowyat.net/index.php?showtopic='+thread_id+'&view=findpost&p='+post_id
            author = textify(post.select('.//span[@class="normalname"]/a/text()'))
            author_ref_url = textify(post.select('.//span[@class="normalname"]/a/@href'))
            if "http:" not in author_ref_url:
                author_ref_url = 'https://forum.lowyat.net'+author_ref_url
            author_ext_info = textify(post.select('.//div[@class="avatar_extra"]//text()'))
            posts = author_ext_info.split(':')[3]
            posts = posts.split(' ')[1]
            group = author_ext_info.split(':')[1]
            author = {'name':xcode(author),'url':author_ref_url}

            item = Item(response)
            item.set('title', xcode(title))
            item.set('text', xcode(text))
            item.set('dt_added', dt_added)
            item.set('author',author)
            item.set('forum',forum)
            item.set('thread',thread)
            item.set('url',url)
            item.set('xtags',['malaysia_country_manual','forums_sourcetype_manual'])
            #print '\n'
            #print response.url
            #print title
            #print author
            #yield item.process()

        try: next_page = hdoc.select('//span[@class="pagecurrent"]/preceding-sibling::span[@class="pagelink"][1]/a/@href').extract()[1]
        except: next_page = ''
        if next_page and is_next:
            url = 'https://forum.lowyat.net'+textify(next_page)
            print url
            yield Request(url,self.parse_thread,response)
