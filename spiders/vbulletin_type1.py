from juicer.forum_utils import *

class VbulletinSpider4(ForumSpider):
    name = "vbulletin_type1"
    #name = 'vbulletin'

    def parse(self, response):

        hdoc = HTML(response)

        forum_url = response.meta.get('url')
        lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

        nodes = hdoc.select('//tbody[contains(@id,"forum")][contains(@id,"bit")]//tr')

        for node in nodes:
            time = textify(node.select('.//div[@align="right"]//text()'))
            if not time:
                time = textify(node.select('.//td[@class="alt2"]/div//text()'))
            if time == '':continue
            time = time.split('by')[0]
            cur_ts = parse_date(time)
            self.latest_timestamp[forum_url] = max(self.latest_timestamp[forum_url], cur_ts)

            if cur_ts <= lastrun_ts:
                continue

            urls = node.select_urls(['.//td[contains(@class,"alt1")]/div/a/@href'],response)
            yield Request(urls, self.parse, response, meta=response.meta)

            next_page_url = hdoc.select('//a[contains(@title,"Next Page")]/@href')
            if next_page_url:
                yield Request(next_page_url, self.parse, response, meta=response.meta)
            terminal_urls = node.select_urls('./td[contains(@id,"threadtitle")]/div/a/@href', response)
            for url in terminal_urls:
                yield Request(url, self.parse_terminal, response, meta=response.meta)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//a[contains(@title,"Last Page")]/@href'):
            last_pg = hdoc.select('//a[contains(@title,"Last Page")]/@href')

            yield Request(last_pg, self.parse_terminal_nfp, response, meta=response.meta)
        else: #Single Page
            for x in self.parse_terminal_nfp(response):
                yield x


    def parse_terminal_nfp(self, response):
        hdoc = HTML(response)

        nodes = hdoc.select('//table[contains(@id,"post")]')
        for node in nodes:
            time = textify(node.select('.//a[contains(@name,"post")]/parent::div/text()'))
            cur_ts = parse_date(time)

            lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))
            if cur_ts > lastrun_ts:
                item = Item(response)

                sk = textify(node.select('./@id')).replace('post','')
                item.set('sk', sk)
                item.set('forum_name', response.meta.get('title'))

                user_name = textify(node.select('.//a[@class="bigusername"]'))
                user_title = textify(node.select('.//a[@class="bigusername"]//parent::div[@id]//parent::td[@nowrap="nowrap"]//div[@class="smallfont"]'))

                item.set('author', {'user_name': username, 'user_title': user_title})
                item.set('posts_count', textify(node.select('.//div[contains(text(),"Posts")]')).split('Posts:')[-1])
                item.set('joined_date', textify(node.select('.//div[contains(text(),"Join")]')))
                item.set('location', textify(node.select('.//div[contains(text(),"Location")]')))
                item.set('post_title', textify(node.select('.//h2[@class="title icon"]')))
                item.set('post_datetime', textify(node.select('.//a[contains(@name,"post")]/parent::div')))
                item.set('comment', textify(node.select('.//div[contains(@id,"post_message")]')))


        if hdoc.select('//a[contains(@title,"Prev Page")]'):
            prev_url = hdoc.select('//a[contains(@title,"Prev Page")]')

            yield Request(prev_url, self.parse_terminal_nfp, response, meta=response.meta)
