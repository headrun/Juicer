from juicer.utils import *

class Blackmagicdesign(JuicerSpider):
    name = 'blackmagicdesign'
    start_urls = ['http://forum.blackmagicdesign.com/']

    def parse(self, response):
        hdoc = HTML(response)

        if self.latest_dt:
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        sub_forums = hdoc.select('//tr[contains(@class,"row")]')
        for sub_forum in sub_forums:
            post_dt = textify(sub_forum.select('.//div[@class="lastpost-details"]//text()'))
            post_dt = post_dt.split('by')[0].strip()
            try: post_dt = parse_date(post_dt)
            except: continue
            if post_dt < self.latest_dt:
                continue

            sub_forum_url = textify(sub_forum.select('.//td[@class="forum"]/h4/a/@href'))
            if sub_forum_url and not sub_forum_url.startswith('http'):
                sub_forum_url = urlparse.urljoin(response.url, sub_forum_url)
            if sub_forum_url:
                yield Request(sub_forum_url, self.parse, response)

            nextpage_url = hdoc.select('//a[contains(text(),"Next")]/@href')
            if nextpage_url:
                yield Request(nextpage_url, self.parse, response)

            threads = sub_forum.select_urls(['.//h4/a[contains(@href,"viewtopic")]/@href'], response)
            for thread in threads:
                yield Request(thread, self.parse_terminal, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//div[@class="pagination"]/span/a'):
            last_pg = hdoc.select('//div[@class="pagination"]/span/a')[-1]

            yield Request(last_pg, self.parse_terminal_nfp, response)
        else: #Single Page
            for x in self.parse_terminal_nfp(response):
                yield x

    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)

        forum_base = hdoc.select('//div[@id="jumpto"]/a')[-1]
        forum_url = textify(forum_base.select('./@href'))
        forum_title = textify(forum_base.select('./text()'))
        forum_id = ''.join(re.findall(r'f=(\d+)', forum_url))
        if not forum_url.startswith('http'):
            forum_url = urlparse.urljoin(response.url, forum_url)

        thread_url = response.url
        thread_id = ''.join(re.findall(r't=(\d+)', thread_url))
        thread_title = textify(hdoc.select('//h2/a/text()'))

        posts = hdoc.select('//div[@id="message"]/div[contains(@id,"p")]')
        for post in posts:
            post_dt = textify(post.select('.//p[@class="author"]/text()'))
            try: post_dt = parse_date(post_dt)
            except: continue
            if post_dt < self.latest_dt:
                continue

            if self.flag: self.update_dt(post_dt)

            item = Item(response)
            raw_sk = textify(post.select('./@id'))
            sk = ''.join(re.findall(r'\d+', raw_sk))
            url = response.url + '#' + raw_sk

            author = textify(post.select('.//div[@class="profile-wrapper"]//a/text()'))
            author_url = textify(post.select('.//div[@class="profile-wrapper"]//a/@href'))
            if not author_url.startswith('http'):
                author_url = urlparse.urljoin(response.url, author_url)

            text = textify(post.select('.//div[@class="message-column postbody"]'))

            item.set('sk', sk)
            item.set('forum.id', forum_id)
            item.set('forum.url', forum_url)
            item.set('forum.title', forum_title)

            item.set('thread.id', thread_id)
            item.set('thread.url', thread_url)
            item.set('thread.title', thread_title)

            item.set('title', thread_title)
            item.set('text', text)
            item.set('url', url)
            item.set('dt_added', post_dt)
            item.set('author.name', author)
            item.set('author.url', author_url) if author_url else ""

            yield item.process()

        if hdoc.select('//div[@class="pagination"]/span/a'):
            prev_url = hdoc.select('//div[@class="pagination"]/span/a')[-1]

            yield Request(prev_url, self.parse_terminal_nfp, response)

