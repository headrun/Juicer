from juicer.forum_utils import *

class PhpbbType2Spider(ForumSpider):
    name = 'phpbb_type2'

    def parse(self, response):
        hdoc = HTML(response)

        forum_url = response.meta.get('url')

        lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

        nodes = hdoc.select('//table[@class="forumline"]//span[@class="forumlink"]//parent::td//parent::tr')

        for node in nodes:
            time = textify(node.select('.//a//parent::span[@class="gensmall"]/text()[contains(string(),":")]')) or textify(node.select('.//a//parent::span[@class="gensmall"]/text()'))

            cur_ts = parse_date(time)

            self.latest_timestamp[forum_url] = max(self.latest_timestamp[forum_url], cur_ts)

            if cur_ts <= lastrun_ts:
                continue

            urls = node.select_urls(['.//a[@class="forumlink"]/@href'], response)
            for url in urls:
                yield Request(url, self.parse, response, meta=response.meta)

        next_url = textify(hdoc.select('//a[contains(text(),"Next")]/@href'))
        next_page_url = next_url.split('\n\n\n')[0]
        if next_page_url:
            yield Request(next_page_url, self.parse, response, meta=response.meta)

        terminal_urls = hdoc.select_urls('//a[@class="topictitle"]/@href', response)
        for url in terminal_urls:
            yield Request(url, self.parse_terminal, response, meta=response.meta)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//span[contains(text(),"Goto page ")]//a[not(contains(text(),"Next"))][last()]/@href'):
            last = textify(hdoc.select('//span[contains(text(),"Goto page ")]//a[not(contains(text(),"Next"))][last()]/@href')).split('\n\n\n')
            last_pg = last[0]

            yield Request(last_pg, self.parse_terminal_details, response, meta=response.meta)

        else:
            for x in self.parse_terminal_details(response):
                yield x

    def parse_terminal_details(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//table[@class="forumline"]//span[@class="name"]//ancestor::tr') or hdoc.select('//table[@class="forumline"]//span[@class="name"]//parent::td//parent::tr')
        for node in nodes:
            time = textify(node.select('.//td[@class]//table//tr//td//span[@class="postdetails"]/text()[contains(string(),"Posted:")]')).split('Posted:')[-1]
            time = time.split(' ')
            time = ' '.join(time)
            cur_ts = parse_date(time)

            lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

            if cur_ts > lastrun_ts:
                item = Item(response, HTML)
                sk = textify(node.select('.//a/@href[contains(string(), "&p=")]')).split('&p=')[-1]
                sk = sk.split(' ')[0]
                item.set('sk', sk)
                #item.set('forum_name', response.meta.get('title'))
                item.set('author', textify(node.select('.//span[@class="name"]//b')))
                posts_count = textify(node.select('.//span[@class="postdetails"]/text()[contains(string(), "Posts:")]')).split('Posts:')[-1]
                item.set('posts_count', posts_count)
                item.set('joined_date', textify(node.select('.//span[@class="postdetails"]/text()[contains(string(), "Joined:")]')).split('Joined:')[-1])
                item.set('location', textify(node.select('.//span[@class="postdetails"]/text()[contains(string(), "Location:")]')).split('Location:')[-1])
                post_date = textify(node.select('.//td[@class]//table//tr//td//span[@class="postdetails"]/text()[contains(string(),"Posted:")]')).split('Posted:')[-1]
                item.set('post_date', post_date)
                comment = textify(node.select('.//span[@class="postbody"]')) or textify(node.select('.//a//parent::span[@class="postbody"]'))
                item.set('comment', repr(comment))
                post_subject = textify(node.select('.//td[@class]//table//tr//td//span[@class="postdetails"]/text()[contains(string(),"Post subject:")]')).split('Post subject:')[-1]
                item.set('post_subject', post_subject)
                item.set('icq_number', textify(node.select('.//img[@title="ICQ Number"]//parent::a/@href'))).split('?to=')[-1]
                item.set('author_website', textify(node.select('.//a[@target="_userwww"]/@href')))
                item.set('image_url', textify(node.select('.//span[@class="postdetails"]//img/@src')))
                yield item.process()

        if hdoc.select('//span[@class="nav"]//a[contains(text(),"Previous")]/@href'):
            prev_url =  hdoc.select('//span[@class="nav"]//a[contains(text(),"Previous")]/@href')

            yield Request(prev_url, self.parse_terminal_details, response, meta=response.meta)
