from juicer.utils import *

class Tipidpc(JuicerSpider):
    name = 'tipidpc'
    start_urls = ['http://www.tipidpc.com/forums.php?sec=1',
                  #'http://www.tipidpc.com/forums.php?sec=2',
                  #'http://www.tipidpc.com/forums.php?sec=3',
                  #'http://www.tipidpc.com/forums.php?sec=4',
                  #'http://www.tipidpc.com/forums.php?sec=5',
                  #'http://www.tipidpc.com/forums.php?sec=6',
                  #'http://www.tipidpc.com/forums.php?sec=7',
                  #'http://www.tipidpc.com/forums.php?sec=8',
                  #'http://www.tipidpc.com/forums.php?sec=15'
                ]

    def parse(self, response):
        hdoc = HTML(response)

        '''
        if self.latest_dt:
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        '''
        threads = hdoc.select('//ul[@class="forumtopics"]/li')

        for thread in threads[:1]:
            post_dt = textify(thread.select('./p[@class="forumtopicmeta"]/text()'))
            post_dt = post_dt.split('on')[-1].strip()
            try: post_dt = parse_date(post_dt)
            except: continue

            #if post_dt < self.latest_dt:
                #continue

            thread_url = textify(thread.select('./h4/a/@href'))
            if thread_url:
                forum_title = textify(hdoc.select('//h2[@class="forumsection"]/span/a/text()'))
                forum_id = ''.join(re.findall(r'sec=(\d+)', response.url))
                print thread_url
                #yield Request(thread_url, self.parse_terminal_nfp,
                        #response, meta = {"forum_url" : response.url, "forum_id" : forum_id, "forum_title" : forum_title})

            nextpage_url = hdoc.select('//input[@value="Next"]/@onclick')
            if not nextpage_url:
                continue
            nextpage_url = hdoc.select('//input[@value="Next"]/@onclick')[-1]
            nextpage_url = eval(textify(nextpage_url).split('href=')[-1])
            #yield Request(nextpage_url, self.parse, response)

    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)

        forum_url = response.meta['forum_url']
        forum_title = response.meta['forum_title']
        forum_id = response.meta['forum_id']

        thread_url = response.url
        thread_id = ''.join(re.findall(r'tid=(\d+)', thread_url))
        thread_title = textify(hdoc.select('//h1[@class="topictitle"]'))

        posts = hdoc.select('//ul[@class="posts"]/li[contains(@id,"post")]')
        for post in posts:
            raw_sk = textify(post.select('./@id'))
            sk = ''.join(re.findall(r'\d+', raw_sk))
            url = response.url + '#' + raw_sk

            post_dt = textify(post.select('./p[@class="postmeta"]/text()'))
            post_dt = post_dt.split('on')[-1].strip()
            if not post_dt: continue
            try:
                post_dt = parse_date(post_dt).replace(tzinfo=None)
                if post_dt < self.latest_dt: continue
            except: continue

            if self.flag: self.update_dt(post_dt)

            item = Item(response)

            author = textify(post.select('./p[@class="postmeta"]/a/text()'))
            author_url = textify(post.select('./p[@class="postmeta"]/a/@href'))
            if not author_url.startswith('http'):
                author_url = urlparse.urljoin(response.url, author_url)

            text = textify(post.select('./div[@class="postcontent"]'))
            if not text:
                continue
            import pdb;pdb.set_trace()
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

            #yield item.process()

        if hdoc.select('//input[@value="Prev"]/@onclick'):
            prev_url = hdoc.select('//input[@value="Prev"]/@onclick')[-1]
            prev_url = eval(textify(prev_url).split('href=')[-1])
            yield Request(prev_url, self.parse_terminal_nfp, response, meta=response.meta)

