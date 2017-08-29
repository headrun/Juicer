from juicer.utils import *
from dateutil import parser

class PakwheelsForum(JuicerSpider):
    name = 'pakwheels_forum'
    start_urls = ['http://www.pakwheels.com/forums/forum.php']

    def parse(self,response):
        hdoc = HTML(response)
        """
        nodes = hdoc.select('//ol[@id="forums"]//li[contains(@id,"forum")]')
        for node in nodes[:4]:
            url = textify(node.select('.//h2/a/@href'))
            forum_title = textify(node.select('.//h2/a/text()'))
            forum_desc = textify(node.select('.//p[@class="forumdescription"]//text()'))
            forum_id = textify(node.select('./@id'))
            forum_id = forum_id.strip('forum')
            forum = {'title':forum_title,'id':forum_id,'url':url,'text':forum_desc}
            print url
            yield Request(url,self.parse_forums,response,meta={'forum':forum})

    def parse_forums(self,response):
        hdoc = HTML(response)
        sub_entry = hdoc.select('//div[@class="forumhead"]/h2//text()')
        forum = response.meta['forum']
        is_crawl = True
        if sub_entry:
            sub_forums = hdoc.select('//div[@id="forumbits"]//li[contains(@id,"forum")]')

            for sub_forum in sub_forums:
                url_sub = textify(sub_forum.select('.//h2/a/@href'))
                forum_title_sub = textify(sub_forum.select('.//h2/a//text()'))
                forum_desc_sub = textify(sub_forum.select('.//p[@class="forumdescription"]//text()'))
                forum_id_sub = textify(sub_forum.select('./@id'))
                forum_id_sub = forum_id_sub.strip('forum')
                forum_sub = {'title':forum_title_sub,'url':url_sub,'id':forum_id_sub,'text':forum_desc_sub}
                yield Request(url_sub,self.parse_forums,response,meta={'forum':forum_sub})

        nodes = hdoc.select('//li[contains(@class,"threadbit")]')

        for node in nodes:
            thread_url = textify(node.select('.//h3/a/@href'))
            thread_id = textify(node.select('./@id'))
            thread_id = thread_id.split('_')[-1]
            thread_name = textify(node.select('.//h3/a//text()'))
            thread_author = textify(node.select('.//div[@class="author"]/span/a/text()'))
            thread_author_url = textify(node.select('.//div[@class="author"]/span/a/@href'))
            thread_started = textify(node.select('.//div[@class="author"]/span//text()'))
            thread_time = thread_started.split(' ')[-1]
            thread_started = re.findall(r'\d{1,2}\-\d{1,2}\-\d{2,4}\xa0\d{1,2}\:\d{1,2}',thread_started)
            thread_started = "".join(thread_started)
            thread_started = xcode(thread_started).replace('\xc2\xa0',' ')+' '+thread_time
            thread = {'url':thread_url,'id':thread_id,'title':thread_name}
            thread_author = {'author':thread_author,'author_url':thread_author_url}
            thread_latest_time = textify(node.select('.//dl[@class="threadlastpost td"]//dd[2]'))
            thread_latest_time = get_timestamp(parse_date(thread_latest_time))
            if thread_latest_time < get_current_timestamp()-86400*10:
                is_crawl = False
                continue
            yield Request(thread_url,self.parse_thread,response,meta={'thread':thread,'forum':forum,'count':1})

        try:
            next_page = textify(hdoc.select('//div[@class="threadpagenav"]//span[@class="prev_next"]/a[@rel="next"]/@href')[0])
            if next_page and is_crawl:
                url = response.url+next_page
                yield Request(next_page,self.parse_forums,response,meta={'forum':forum})
        except:
            pass

    def parse_thread(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="pagetitle"]/h1//a//text()'))
        thread = response.meta['thread']
        forum = response.meta['forum']
        is_next = True

        last_page = hdoc.select('//div[@id="pagination_top"]//span[@class="first_last"]//a/@href')
        if last_page:
            yield Request(last_page,self.parse_thread,response,meta={'count':1,'thread':thread,'forum':forum})

        try:
            count = response.meta['count']
            nodes = hdoc.select('//ol[@id="posts"]/li[contains(@id,"post")]')
        except:
            nodes = hdoc.select('//ol[@id="posts"]/li[contains(@id,"post")][position()>1]')

        for node in nodes:
            date = textify(node.select('.//div[@class="posthead"]//span[@class="date"]//text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5))
            if dt_added < get_current_timestamp()-86400*10:
                is_next = False
                continue
            if dt_added > get_current_timestamp()-86400*7:
                continue
            post_id = textify(node.select('./@id'))
            post_url = response.url+'#'+post_id
            author_url = textify(node.select('.//div[@class="postdetails"]//div[@class="username_container"]//a/@href'))
            author_name = textify(node.select('.//div[@class="postdetails"]//div[@class="username_container"]//a//text()'))
            author_title = textify(node.select('.//div[@class="postdetails"]//span[@class="usertitle"]//text()'))
            author_ext_info = node.select('.//div[@class="postdetails"]/div[@class="userinfo"]/dl[@class="userinfo_extra"]//dt')
            author_ext_info_data = node.select('.//div[@class="postdetails"]/div[@class="userinfo"]/dl[@class="userinfo_extra"]//dd')
            join_date = ''
            age = ''
            posts = ''
            location = ''
            mentioned = ''
            tagged = ''
            follows = ''
            following = ''

            for author_info in author_ext_info:
                match = textify(author_info.select('./text()'))
                if match == 'Join Date':
                    join_date = textify(author_info.select('./following-sibling::dd[1]/text()'))
                if match == 'Location':
                    location = textify(author_info.select('./following-sibling::dd[1]/text()'))
                if match == 'Age':
                    age = textify(author_info.select('./following-sibling::dd[1]/text()'))
                if match == 'Posts':
                    posts = textify(author_info.select('./following-sibling::dd[1]/text()'))
                if match == 'Mentioned':
                    mentioned = textify(author_info.select('./following-sibling::dd[1]/text()'))
                if match == 'Tagged':
                    tagged = textify(author_info.select('./following-sibling::dd[1]/text()'))
                if match == 'Follows':
                    follows = textify(author_info.select('./following-sibling::dd[1]/text()'))
                if match == 'Following':
                    following = textify(author_info.select('./following-sibling::dd[1]/text()'))
            author = {'name':author_name,'url':author_url,'join_date':join_date,'age':age,'posts':posts,'location':location,'mentioned':mentioned,'tagged':tagged,'follows':follows,'following':following,'title':author_title}
            text = textify(node.select('.//div[@class="postdetails"]//div[@class="content"]//text()'))


            #if dt_added < get_current_timestamp()-86400*10:
                #is_next = False


            item = Item(response)
            item.set('title', title)
            item.set('text',xcode(text))
            item.set('dt_added',dt_added)
            item.set('author',author)
            item.set('url',post_url)
            item.set('forum',forum)
            item.set('thread',thread)
            item.set('sk',md5(post_url))
            item.set('xtags', ['forums_sourcetype_manual', 'pakistan_country_manual'])
            #yield item.process()
            print post_url
            print date

        try:
            next_page = hdoc.select('//div[@id="pagination_top"]//span[@class="prev_next"]/a[@rel="prev"]/@href')
            if next_page and is_next:
                yield Request(next_page,self.parse_thread,response,meta={'forum':forum,'thread':thread})
        except:
            pass
            """
