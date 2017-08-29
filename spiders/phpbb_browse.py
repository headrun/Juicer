from juicer.forum_utils import *

class PhpbbSpider(ForumSpider):
    name = 'phpbb'

    def parse(self, response):
        hdoc = HTML(response)

        self.lastrun_ts = None
        forum_url = response.meta.get('url')

        self.lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

        nodes = hdoc.select('//dl[@class="icon"]')

        for node in nodes:
            time = textify(node.select('.//dd[@class="lastpost"]//span/text()\
                    [not(contains(string(),"by"))][not(contains(string(),"post"))]'))

            cur_ts = parse_date(time)

            self.latest_timestamp[forum_url] = max(self.latest_timestamp[forum_url], cur_ts)

            if cur_ts <= self.lastrun_ts:
                continue

            urls = node.select_urls(['.//dt//a[@class="forumtitle"]/@href'], response)
            yield Request(urls, self.parse, response, meta=response.meta)

            next_page_url = hdoc.select('//form[@method="post"]//a[contains(text(),"Next")]/@href')
            if next_page_url:
                yield Request(next_page_url, self.parse, response, meta=response.meta)

            forum_title = textify(hdoc.select('//div[@id="page-body"]/h2/a'))
            forum_id = ''.join(re.findall(r'php\?f=(\d+)', response.url))

            response.meta['forum_title'] = forum_title
            response.meta['forum_url'] = response.url
            response.meta['forum_id'] = forum_id

            terminal_urls = node.select_urls('.//dt//a[@class="topictitle"]/@href', response)
            for url in terminal_urls:
                yield Request(url, self.parse_terminal, response, meta=response.meta)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//div[@class="pagination"]//span//a[last()]/@href'): # if last_page link is present
            last = textify(hdoc.select('//div[@class="pagination"]//span//a[last()]/@href')).split(' ')
            last_pg = last[0]

            yield Request(last_pg, self.parse_terminal_nfp, response, meta=response.meta)

        else: #Single Page
            for x in self.parse_terminal_nfp(response):
                yield x

    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)

        cnode = hdoc.select('//div[@id="page-body"]')
        nodes = cnode.select('.//div[@class="inner"]')

        for node in nodes:
            time = textify(node.select('.//div[@class="postbody"]//p[@class="author"]/\
                    text()[not(contains(string(),"by "))]')).split(' ')[1:]
            time = ' '.join(time)
            post_dt = parse_date(time)

            if post_dt < self.lastrun_ts:
                continue

            item = Item(response, HTML)

            link = textify(node.select('.//div[@class="postbody"]//h3//a/@href'))
            sk = link.split('#p')[-1]
            post_url = re.sub(r'\?f=.*','', response.url) + '?p=' + sk + link

            author = textify(node.select('.//dl[@class="postprofile"]//a')).strip()
            author_url = textify(node.select('.//dl[@class="postprofile"]//a[1]/@href'))
            author_url = urlparse.urljoin(response.url, author_url)
            posts_count = textify(node.select('.//strong[contains(text(),"Posts:")]//parent::dd')).split('Posts:')[-1]
            location = textify(node.select('.//strong[contains(text(),"Location:")]//parent::dd')).split('Location:')[-1]
            joined_dt = textify(node.select('.//strong[contains(text(),"Joined:")]//parent::dd')).split('Joined:')[-1]
            joined_dt = parse_date(joined_dt.strip())

            text = textify(node.select('.//div[@class="content"]'))
            title = textify(node.select('.//div[@class="postbody"]//h3//a'))
            thread_title = textify(hdoc.select('//div[@id="page-body"]/h2/a'))
            thread_id = ''.join(re.findall(r'php\?f=\d+&t=(\d+)', response.url))

            item.set('sk', sk)
            item.set('forum.id', response.meta.get('forum_id'))
            item.set('forum.tilte', response.meta.get('forum_title'))
            item.set('forum.url', re.sub(r'&sid=.*', '', response.meta.get('forum_url')))

            item.set('thread.id', thread_id)
            item.set('thread.title', thread_title)
            item.set('thread.url', re.sub(r'&sid=.*', '', response.url))

            item.set('url', re.sub(r'&sid=.*', '', post_url))
            item.set('title', thread_title)
            item.set('text', text)

            item.set('author.name', xcode(author))
            item.set('author.url', xcode(re.sub(r'&sid=.*', '', author_url))) if author_url else ""
            item.set('author.num.posts', int(re.sub(r'\,','',posts_count))) if posts_count else ''
            item.set('author.location', location.strip()) if location else ''
            item.set('author.join_dt', joined_dt) if joined_dt else ''
            item.set('dt_added', post_dt)

            ob = pprint.PrettyPrinter(indent=2)
            ob.pprint(item.data)

        if hdoc.select('//form[@method="post"]//a[contains(text(),"Previous")]/@href'):
            prev_url =  hdoc.select('//form[@method="post"]//a[contains(text(),"Previous")]/@href')
            yield Request(prev_url, self.parse_terminal_nfp, response, meta=response.meta)
