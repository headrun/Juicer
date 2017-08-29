from juicer.forum_utils import *

class PhpbbSpider(ForumSpider):
    name = 'phpbb_bkup'

    def parse(self, response):
        hdoc = HTML(response)

        forum_url = response.meta.get('url')

        lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

        nodes = hdoc.select('//dl[@class="icon"]')

        for node in nodes:
            time = textify(node.select('.//dd[@class="lastpost"]//span/text()[not(contains(string(),"by"))][not(contains(string(),"post"))]'))

            cur_ts = parse_date(time)

            self.latest_timestamp[forum_url] = max(self.latest_timestamp[forum_url], cur_ts)

            if cur_ts <= lastrun_ts:
                continue

            urls = node.select_urls(['.//dt//a[@class="forumtitle"]/@href'], response)
            yield Request(urls, self.parse, response, meta=response.meta)

            next_page_url = hdoc.select('//form[@method="post"]//a[contains(text(),"Next")]/@href')
            if next_page_url:
                yield Request(next_page_url, self.parse, response, meta=response.meta)

            terminal_urls = node.select_urls('.//dt//a[@class="topictitle"]/@href', response)
            for url in terminal_urls:
                yield Request(url, self.parse_terminal, response, meta=response.meta)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//div[@class="pagination"]//span//a[last()]/@href'): # if last_page link is present
            last = textify(hdoc.select('//div[@class="pagination"]//span//a[last()]/@href')).split('\n\n\n')
            last_pg = last[0]

            yield Request(last_pg, self.parse_terminal_nfp, response, meta=response.meta)

        else: #Single Page
            for x in self.parse_terminal_nfp(response):
                yield x

    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)
        #import pdb; pdb.set_trace()
        cnode = hdoc.select('//div[@id="page-body"]')
        nodes = cnode.select('.//div[@class="inner"]')
        for node in nodes:
            time = textify(node.select('.//div[@class="postbody"]//p[@class="author"]/text()[not(contains(string(),"by "))]')).split(' ')[1:]
            time = ' '.join(time)
            cur_ts = parse_date(time)

            lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

            if cur_ts > lastrun_ts:
                item = Item(response)
                sk = textify(node.select('.//div[@class="postbody"]//h3//a/@href')).split('#p')[-1]
                item.set('sk', sk)
                item.set('forum_name', response.meta.get('title'))
                item.set('author', node.select('.//dl[@class="postprofile"]//a/@href'))
                item.set('posts_count', textify(node.select('.//strong[contains(text(),"Posts:")]//parent::dd')).split('Posts:')[-1])
                item.set('joined_date', textify(node.select('.//strong[contains(text(),"Joined:")]//parent::dd')).split('Joined:')[-1])
                item.set('cash_on_hand', textify(node.select('.//strong[contains(text(),"Cash on hand:")]//parent::dd')).split('Cash on hand:')[-1])
                item.set('bank', textify(node.select('.//strong[contains(text(),"Bank:")]//parent::dd')))
                item.set('location', textify(node.select('.//strong[contains(text(),"Location:")]//parent::dd')).split('Location:')[-1])
                item.set('post_title', textify(node.select('.//div[@class="postbody"]//h3//a')))
                item.set('post_date', textify(node.select('.//div[@class="postbody"]//p[@class="author"]/text()[not(contains(string(),"by "))]')))
                item.set('comment', textify(node.select('.//div[@class="content"]')))
                item.process()

        if hdoc.select('//form[@method="post"]//a[contains(text(),"Previous")]/@href'):
            prev_url =  hdoc.select('//form[@method="post"]//a[contains(text(),"Previous")]/@href')

            yield Request(prev_url, self.parse_terminal_nfp, response, meta=response.meta)
