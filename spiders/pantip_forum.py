import json
from juicer.utils import *

class Pantip(JuicerSpider):
    name = 'pantip'
    start_urls = ['http://pantip.com/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes =  hdoc.select('//div[@class="submenu-room"]//ul[@class="submenu-room-list"]//li[@class="submenu-room-item"]')
        self.cutoff_dt = datetime.datetime.utcnow() - datetime.timedelta(days=2)
        for node in nodes:
            node = node.select('.//a//@href')
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        threads = hdoc.select('//div[@class="post-list-wrapper"]/div[contains(@class, "post-item")]')
        is_next = True
        forum = {}
        forum['url'] = response.url.split('?')[0]
        forum['title'] = textify(hdoc.select('//div[@class="content"]//li[@class="last"]//text()'))

        for thread in threads:
            post_date = textify(thread.select('.//div[@class="post-item-by"]//span[@class="timestamp"]//abbr/@data-utime'))
            post_date = parse_date(post_date)
            if post_date > self.cutoff_dt:
                url= textify(thread.select('.//div[@class="post-item-title"]//a/@href'))
                yield Request(url,self.parse_post_details,response, meta={'forum': forum})
            else:
                is_next = False

        next_url = textify(hdoc.select('//div[@class="loadmore-bar indexlist"]/a/@href'))
        if next_url and is_next:
            yield Request(next_url,self.parse_next,response)

    def generate_item(self, title, text, dt_added, author, url, thread, forum, response):

        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=7))
        """
        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('author', author)
        item.set('url', url)
        item.set('forum', forum)
        item.set('thread', thread)
        return item
        """
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'author',xcode(author)
        print 'url',xcode(url)
        import pdb;pdb.set_trace()
    def parse_post_details(self,response):
        hdoc = HTML(response)

        _id = response.url.split('/')[-1]
        title = textify(hdoc.select('//h2[@class="display-post-title"]//text()'))
        text = textify(hdoc.select('//div[@class="display-post-story"]/text()'))
        author_name = textify(hdoc.select('//a[@class="display-post-name owner"]//text()'))
        author_url = textify(hdoc.select('//a[@class="display-post-name owner"]//@href'))
        author_id = author_url.split('/')[-1]
        dt_added = textify(hdoc.select('//span[@class="display-post-timestamp"]//abbr//@data-utime'))
        if u'\u0e2a\u0e21\u0e32\u0e0a\u0e34\u0e01\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02' in author_name:
            author_name = " "

        thread = {}
        thread['id'] = _id
        thread['title'] = title
        thread['url'] = response.url
        forum = response.meta['forum']
        author = {}
        author['id'] = author_id
        author['name'] = author_name
        author['url'] = author_url

        item = self.generate_item(title, text, dt_added, author, response.url, thread, forum, response)
        yield item.process()

        headers ={'Referer': response.url, 'X-Requested-With':'XMLHttpRequest', 'User-Agent':'Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/32.0.1700.107 Chrome/32.0.1700.107 Safari/537.36', 'Accept':'application/json, text/javascript, */*; q=0.01', 'Host':'pantip.com', 'Accept-Encoding':'gzip,deflate,sdch', 'Accept-Language':'en-US,en;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'method':'GET'}

        url = "http://pantip.com/forum/topic/render_comments?tid=%s&param=&type=3" %_id
        yield Request(url,self.parse_post_response, headers=headers, meta={'thread':thread, 'forum':forum})

    def parse_post_response(self,response):
        data = json.loads(response.body)
        comments = data.get('comments', [])
        for comment in comments:
            _dt_added = comment['data_utime']
            _dt_added = parse_date(_dt_added)
            if _dt_added < self.cutoff_dt:
                continue

            title = response.meta['thread']['title']
            text = comment.get('message', '')
            url = '%s#comment%s' %(response.meta['thread']['url'], comment.get('comment_no',''))
            author = {}
            author['name'] = comment['user']['name']
            author['url'] = 'http://pantip.com/%s' %comment['user']['link']
            author['id'] = comment['user']['link'].split('/')[-1]
            if u'\u0e2a\u0e21\u0e32\u0e0a\u0e34\u0e01\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02' in author['name']:
                author['name'] = ''
            dt_added = comment['data_utime']

            item = self.generate_item(title, text, dt_added, author, url, response.meta['thread'], response.meta['forum'], response)
            yield item.process()

        if comments and data['count']>100 and data['paging']['page']== 1:
            headers ={'Referer': response.meta['thread']['url'], 'X-Requested-With':'XMLHttpRequest', 'User-Agent':'Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/32.0.1700.107 Chrome/32.0.1700.107 Safari/537.36', 'Accept':'application/json, text/javascript, */*; q=0.01', 'Host':'pantip.com', 'Accept-Encoding':'gzip,deflate,sdch', 'Accept-Language':'en-US,en;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'method':'GET'}
            url = "http://pantip.com/forum/topic/render_comments?tid=%s&param=page2&type=1&page=2&parent=2&expand=1" %response.meta['thread']['id']
            yield Request(url,self.parse_post_response, headers=headers, meta={'thread':response.meta['thread'], 'forum':response.meta['forum']})
