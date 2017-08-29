from juicer.forum_utils import *

class VbulletinType2Spider(ForumSpider):
    name = 'vbulletin_type2'

    def parse(self, response):

        hdoc = HTML(response)

        forum_url = response.meta.get('url')
        lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

        nodes = hdoc.select('//td[@class="alt2"]//parent::tr[@align="center"]')

        for node in nodes:
            time = textify(node.select('.//div[@align="right"]/text()')).strip()
            if not time:
                time = textify(node.select('.//td[@class="alt2"]/div//text()')).strip()
            if time == '':
                continue
            #time = time.split('by')[0]
            #time = time.split('PM'[0]
            #import pdb; pdb.set_trace()
            cur_ts = parse_date(time)
            self.latest_timestamp[forum_url] = max(self.latest_timestamp[forum_url], cur_ts)

            if cur_ts <= lastrun_ts:
                continue

            urls = node.select_urls(['.//td[@align="left"]//div[not(contains(@class, "smallfont"))]//a/@href'],response)
            for url in urls:
                yield Request(urls, self.parse, response, meta=response.meta)

        next_page_url = textify(hdoc.select('//a[contains(@title,"Next ")]/@href')).split('\n\n\n')
        next_page_url = next_page_url[0]
        if next_page_url:
            yield Request(next_page_url, self.parse, response, meta=response.meta)

        terminal_urls = hdoc.select_urls('//td[contains(@id,"threadtitle")]/div/a/@href', response)
        for url in terminal_urls:
            yield Request(url, self.parse_terminal, response, meta=response.meta)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//a[contains(text(), "Last ")]/@href'):
            last_pg = textify(hdoc.select('//a[contains(text(), "Last ")]/@href')).split('\n\n\n')
            last_pg = last_pg[0]

            yield Request(last_pg, self.parse_terminal_details, response, meta=response.meta)
        else: #Single Page
            for x in self.parse_terminal_details(response):
                yield x


    def parse_terminal_details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        thread_title = textify(hdoc.select('//td[@class="navbar"]//strong'))
        item.textify('thread_title', '//td[@class="navbar"]//strong')
        nodes = hdoc.select('//table[contains(@id,"post")]')
        for node in nodes:
            time = textify(node.select('.//img[@class="inlineimg"]//ancestor::td[@class="thead"]/text()')).strip()
            cur_ts = parse_date(time)

            lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))
            if cur_ts > lastrun_ts:
                sk = textify(node.select('./@id')).replace('post','')
                item.set('sk', sk)
                author = textify(node.select('.//a[@class="bigusername"]'))
                item.set('author', author)
                post_count = textify(node.select('.//div[contains(text(),"Posts")]')).split('Posts:')[-1]
                post_count = ' ' + '---'.join(post_count.split())
                item.set('post_count', post_count)
                joined_date =  textify(node.select('.//div[contains(text(),"Join")]')).split('Join Date:')
                item.set('joined_date', joined_date)
                location = textify(node.select('.//div[contains(text(),"Location")]')).split('Location:')
                item.set('location', location)
                item.set('post_title', textify(node.select('.//div[@class="smallfont"]//strong')))
                item.set('post_datetime', textify(node.select('.//img[@class="inlineimg"]//ancestor::td[@class="thead"]/text()')))
                item.set('comment', textify(node.select('.//div[contains(@id,"post_message")]')))
                post_counter = textify(node.select('.//a[@target="new"]//strong'))
                post_counter = thread_title + '#' + post_counter
                item.set('post_counter', post_counter)
                yield item.process()

        if hdoc.select('//a[contains(@title,"Prev ")]'):
            prev_url = hdoc.select('//a[contains(@title,"Prev ")]').split('\n\n\n')
            prev_url = prev_url[0]

            yield Request(prev_url, self.parse_terminal_details, response, meta=response.meta)
