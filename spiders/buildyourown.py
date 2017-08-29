from juicer.utils import *
from dateutil import parser


class Buildyourown(JuicerSpider):
    name = 'buildyourown'
    start_urls = ['https://forum.buildyourown.org.uk/']

    def parse(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        if self.latest_dt:
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        subforums = hdoc.select('//tr/td[contains(@class,"spnMessageText")]/a/ancestor::tr')
        for sub_forum in subforums[:2]:
            import pdb;pdb.set_trace()
            post_dt = textify(sub_forum.select('./td/span[@class="spnMessageText"]/parent::td//text()'))
            post_dt = post_dt.split('by')[0].strip()

            if not post_dt: continue

            try: post_dt = parse_date(post_dt)
            except: continue

            if post_dt < self.latest_dt:
                continue

            sub_forum_url = textify(sub_forum.select('./td[contains(@class,"spnMessageText")]/a/@href'))
            yield Request(sub_forum_url, self.parse, response)

            if 'forum_id' in response.url.lower():
                pagination = ''.join(re.findall(r'whichpage=(\d+)', response.url))
                if pagination:
                    nextpage_url = re.sub(r'whichpage=(\d+)', '', response.url) + '' + str(int(pagination)+1)
                else: nextpage_url = response.url + '&sortfield=lastpost&sortorder=&whichpage=2'
                yield Request(nextpage_url, self.parse, response)

            terminal_urls = sub_forum.select_urls(['./td[contains(@class,"spnMessageText")]/a/@href'], response)
            for url in terminal_urls:
                if not 'topic_id' in url: continue
                yield Request(url, self.parse_terminal, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//select[@name="whichpage"]/option/@value'):
            last_pg = textify(hdoc.select('//select[@name="whichpage"]/option/@value')[-1])
            last_pg = response.url + '&whichpage=' + last_pg

            yield Request(last_pg, self.parse_terminal_nfp, response)
        else: #Single Page
            for x in self.parse_terminal_nfp(response):
                yield x

    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        forum_base = hdoc.select('//h2')
        forum_url = textify(forum_base.select('./a/@href'))
        forum_title = textify(forum_base.select('./a/text()'))
        forum_id = ''.join(re.findall(r'forum_id=(\d+)', forum_url.lower()))

        thread_url = response.url
        thread_id = ''.join(re.findall(r'topic_id=(\d+)', thread_url.lower()))
        thread_title = textify(hdoc.select('//h1/text()'))

        posts = hdoc.select('//table[@class="TableBorderColor"]/tr')

        for post in posts:
            post_dt = textify(post.select('.//td[@class="ForumFontColor FooterFontSize"]/text()'))
            post_date = ''.join(re.findall(r'\d+\s\w+\s[0-9]+', post_dt.replace('Posted', '')))
            post_time = ''.join(re.findall(r'[0-9]+:[0-9]+:[0-9]+', post_dt))
            post_dt = post_date + ' ' + post_time
            if not post_dt: continue

            try: post_dt = parse_date(post_dt)
            except: continue
            if post_dt < self.latest_dt:
                continue

            if self.flag: self.update_dt(post_dt)

            #item = Item(response)
            sk = textify(post.select('.//a[contains(@href, "Reply")]/@href'))
            sk = ''.join(re.findall(r'REPLY_ID=(\d+)', sk))
            url = response.url + '#' + sk if sk else response.url
            sk = hashlib.md5(response.url).hexdigest() if not sk else sk

            author = textify(post.select('.//td[contains(@class,"CellBorderColor")]//p//span[@class="spnMessageText"]/a/text()'))

            author_url = textify(post.select('.//td[contains(@class,"CellBorderColor")]//p//span[@class="spnMessageText"]/a/@href'))

            text = textify(post.select('.//span[@id="msg"]//text()'))
            if not text:
                continue

            forum_url = urlparse.urljoin(response.url, forum_url) if not forum_url.startswith('http') else forum_url
            author_url = urlparse.urljoin(response.url, author_url) if not author_url.startswith('http') else author_url

            ''' item.set('sk', sk)
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

            yield item.process()'''
            if hdoc.select('//a[contains(text(),"Previous Page")]'):
                prev_url = hdoc.select('//a[contains(text(),"Previous Page")]/@href')

            yield Request(prev_url, self.parse_terminal_nfp, response)

