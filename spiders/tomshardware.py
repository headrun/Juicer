from juicer.utils import *

class Tomshardware(JuicerSpider):
    name = 'tomshardware'
    start_urls = ['http://www.tomshardware.com/forum/']

    def parse(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        category_links = hdoc.select('//div[@class="home-table__row category"]/div/a/@href').extract()
        sub_category_links = hdoc.select('//div[@class="home-table__row category"]/div/div[@class="category__subcategories"]/a/@href').extract()

        all_categories = category_links + sub_category_links
        for link in all_categories[:3]:
            if 'http' not in link:
                link ='http://www.tomshardware.com'+link
            yield Request(link, self.parse_terminal, response)


    def parse_terminal(self, response):
        hdoc = HTML(response)
        thread_links = hdoc.select('//tbody/tr[contains(@class,"hlisting")]')
        for thread_link in thread_links[:1]:
            link = textify(thread_link.select('./td[@class="thread-info"]//a[@class="thread-link font116"]/@href'))
            date = textify(thread_link.select('./td[@class="thread-stats txtCenter"]//time[@class="dateTime"]/@title'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            yield Request(link,self.parse_terminal_nfp,response)

        next_page = textify(hdoc.select('//li[@class="nextPage"]/a/@href'))
        if next_page:
            yield Request(next_page,parse_terminal,response)


    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)
        forum_base = hdoc.select('//li[@class="breadcrumbItem"]')[-1]
        forum_url = textify(forum_base.select('./a/@href'))
        forum_title = textify(forum_base.select('./a/text()'))
        forum_id = ''.join(re.findall(r'forum-(\d+)', forum_url))

        thread_url = response.url
        thread_id = ''.join(re.findall(r'id-(\d+)', thread_url))
        thread_id = ''.join(re.findall(r'forum/(\d+)', thread_url)) if not thread_id else thread_id
        thread_id = ''.join(re.findall(r'\d+', thread_url)) if not thread_id else thread_id
        thread_title = textify(hdoc.select('//li[@class="breadcrumbItem noLink"]//text()'))


        print 'forum_url',xcode(forum_url)
        print 'forum_id',xcode(forum_id)
        print 'forum_title',xcode(forum_title)

        print 'thread_url',xcode(thread_url)
        print 'thread_id',xcode(thread_id)
        print 'thread_title',xcode(thread_title)

        posts = hdoc.select('//article[contains(@class,"frmTopicAnswer message")]')
        for post in posts:
            post_dt = textify(post.select('.//span[@class="dateTime lzLink"]/text()'))


            dt_added = get_timestamp(parse_date(xcode(post_dt)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue


            item = Item(response)
            url = textify(post.select('.//time[@class="dateTime"]/parent::a/@href'))
            url = response.url + url
            sk = textify(post.select('./@id'))

            author = textify(post.select('.//a/span[@itemprop="name"]/text()'))
            if not author:
                textify(post.select('.//span[@itemprop="name"]/text()'))
            author_url = textify(post.select('.//a/span[@itemprop="name"]/parent::a/@href'))

            text = textify(post.select('.//div[@class="responseText"]//text()'))

            tag = hdoc.select('//div[@class="bottom-subcateg-links spaceB30"]/ul//li/a/text()')
            tags = [xcode(textify(i).replace("&amp;","&")) for i in tag]

            print 'post_dt',xcode(post_dt)
            print 'url',xcode(url)
            print 'author',xcode(author)
            print 'author_url',xcode(author_url)
            print 'text',xcode(text)
            print 'tags',xcode(tags)


        next_page = textify(hdoc.select('//li[@class="nextPage"]/a/@href'))
        if next_page:
            yield Request(next_page,callback=self.parse_terminal_nfp,response)
