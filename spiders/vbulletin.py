from juicer.forum_utils import *
import pprint

class VbulletinNewSpider(ForumSpider):
    name = 'vbulletin'

    def parse(self, response):
        hdoc = HTML(response)

        self.lastrun_ts = None
        forum_url = response.meta.get('url')
        self.lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

        rows = hdoc.select('//div[@class="forumlastpost td"]/parent::div')

        for row in rows:
            posted_date = textify(row.select('.//p[@class="lastpostdate"]//text()'))
            post_dt = parse_date(posted_date)
            self.latest_timestamp[forum_url] = max(self.latest_timestamp[forum_url], post_dt)
            if post_dt <= self.lastrun_ts:
                continue
            urls = row.select_urls(['.//div[@class="datacontainer"]//a/@href'], response)
            yield Request(urls, self.parse_subforum, response, meta=response.meta)

    def parse_subforum(self, response):
        hdoc = HTML(response)

        forum_urls = hdoc.select_urls(['//h2[@class="forumtitle"]/@href'], response)
        if forum_urls:yield Request(forum_urls, self.parse, response, meta=response.meta)

        nextpage_url = ""
        threads = hdoc.select('//li[contains(@id, "thread_")]')
        if not threads:
            threads = hdoc.select('//tr[contains(@id, "thread_")]')
        for thread in threads:
            posted_time = thread.select('.//dd/span[@class="time"]//parent::dd//text()')
            posted_time = parse_date(textify(posted_time))
            if posted_time < self.lastrun_ts:
                continue

            next_url = hdoc.select('//div[@id="above_threadlist"]//a[contains(@title,"Next")]/@href')
            next_url1 = hdoc.select('//a[contains(@title,"Next")]/@href')
            nextpage_url = textify(next_url)
            url = textify(thread.select('.//a[contains(@id, "thread_")]/@href'))
            views = ''.join(re.findall(r'\d+', textify(thread.select('.//li[contains(text(),"Views")]'))))
            views = int(re.sub(r'\,','', views)) if views else 0

            f_id = hdoc.select('//form[@id="thread_inlinemod_form"]/@action')
            forum_id = "".join(re.findall(r'forumid=(\d+)', textify(f_id)))
            forum_title = textify(hdoc.select('//li[@class="navbit lastnavbit"]'))

            response.meta['forum_id'] = forum_id
            response.meta['forum_title'] = forum_title
            response.meta['forum_url'] = response.url
            response.meta['views'] = views
            yield Request(url, self.parse_terminal, response, meta=response.meta)

        if nextpage_url:
            yield Request(nextpage_url, self.parse_subforum, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        nextpage_url = ""
        next_url = hdoc.select('//div[@class="pagination_top"]//a[contains(@title, "Next Page")]/@href')
        nextpage_url = textify(next_url)

        thread_id = ''.join(re.findall(r'.*/\w+/.*-(\d+)', response.url))
        if not thread_id:
            thread_id = ''.join(re.findall(r'.*/(\d+).*', response.url))
            if not thread_id:
                thread_id = ''.join(re.findall(r'.*/showthread.php\?(\d+).*', response.url))
                if not thread_id:
                    thread_id = ''.join(re.findall(r'.*/showthread.php\?t=(\d+).*', response.url))

        thread_title = textify(hdoc.select('//li[@class="navbit lastnavbit"]//span/text()'))

        nodes = hdoc.select('//li[contains(@id,"post_")]')
        for node in nodes:
            item = Item(response, HTML)
            time = textify(node.select('.//span[@class="date"]//text()')).split('\n\n\n')
            cur_ts = parse_date(' '.join(time))

            if cur_ts < self.lastrun_ts:
                continue

            text = node.select('.//div[contains(@id,"post_message_")]\
                    //blockquote[contains(@class,"postcontent")]//text()')
            text = textify(text).encode('utf8').decode('ascii','ignore')
            text = re.sub(r' +', " ", text.replace("&amp;", "&").replace("\t"," "))
            text = text.replace("&lt;","<").replace("&gt;",">")
            if not text:
                continue
            author = node.select('.//div[@class="username_container"]')
            author_name = textify(author.select('.//a[contains(@class,"username")]//strong//text()'))
            if not author_name:
                author_name = textify(author.select('.//span[@class="username guest"]//text()'))
            author_url = textify(author.select('.//a[contains(@class,"username")]/@href'))
            author_url = urlparse.urljoin(response.url, author_url)
            total_posts = xcode(textify(node.select('.//dl[@class="userinfo_extra"]/dt\
                            [contains(text(),"Posts")]/following-sibling::dd[1]/text()')))

            post_id = textify(node.select('.//div[contains(@id,"post_message_")]/@id'))
            post_url = response.url+"#"+xcode(post_id)

            tag = hdoc.select('//div[@class="inner_block"]//div[@id="tag_list_cell"]//a//text()')
            tags = [xcode(textify(i).replace("&amp;","&")) for i in tag]

            item.set('forum.id', response.meta.get('forum_id'))
            item.set('forum.tilte', response.meta.get('forum_title'))
            item.set('forum.url', response.meta.get('forum_url'))

            item.set('thread.id', thread_id)
            item.set('thread.title', thread_title)
            item.set('thread.url', response.url)
            item.set('num.views', response.meta.get('views')) if response.meta.get('views') else ''

            item.set('url', post_url)
            item.set('title', thread_title)
            item.set('text', text)
            item.set('dt_added', cur_ts)
            item.set('tags', tags) if tags else ''

            item.set('author.name', xcode(author_name))
            item.set('author.url', xcode(author_url)) if author_url else ""
            item.set('author.num.posts', int(re.sub(r'\,','',total_posts))) if total_posts else ''

            yield item.process()

        if nextpage_url:
            yield Request(nextpage_url, self.parse_terminal, response, meta=response.meta)
