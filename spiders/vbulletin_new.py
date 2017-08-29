from juicer.forum_utils import *

class VbulletinNewSpider(ForumSpider):
    name = 'vbulletin_new'

    def parse(self, response):
        hdoc = HTML(response)

        forum_url = response.meta.get('url')
        lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

        nodes = hdoc.select('//div[@class="forumlastpost td"]/parent::div')

        for node in nodes:
            time = textify(node.select('.//p[@class="lastpostdate"]//text()')).split('\n\n\n')
            time = ' '.join(time)

            cur_ts = parse_date(time)

            self.latest_timestamp[forum_url] = max(self.latest_timestamp[forum_url], cur_ts)

            if cur_ts <= lastrun_ts:
                continue
            urls = node.select_urls(['.//h2[@class="forumtitle"]//a/@href'], response)
            yield Request(urls, self.parse, response, meta=response.meta)

        next_url = textify(hdoc.select('//a[@rel="next"]/@href'))
        next_page_url = next_url.split('\n\n\n')[0]
        if next_page_url:
            yield Request(next_page_url, self.parse, response, meta=response.meta)

        terminal_urls = hdoc.select_urls('//h3[@class="threadtitle"]//a/@href', response)
        for url in terminal_urls:
            yield Request(url, self.parse_terminal, response, meta=response.meta)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        if hdoc.select('//a[contains(text(),"Last")]/@href'):
            last = textify(hdoc.select('//a[contains(text(),"Last")]/@href')).split('\n\n\n')
            last_pg = last[0]

            yield Request(last_pg, self.parse_terminal_details, response, meta=response.meta)

        else:
            for x in self.parse_terminal_details(response):
                yield x

    def parse_terminal_details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        thread_title = textify(hdoc.select('//span[@class="threadtitle"]//a'))
        item.set('thread_title', thread_title)
        nodes = hdoc.select('//div[@class="posthead"]//parent::li[@class]')
        for node in nodes:
            time = textify(node.select('.//span[@class="date"]//text()')).split('\n\n\n')
            time = ' '.join(time)
            item.set('time', time)
            cur_ts = parse_date(time)

            lastrun_ts = datetime.datetime.fromtimestamp(response.meta.get('last_run'))

            if cur_ts > lastrun_ts:
                sk = textify(node.select('.//div[@class="popupmenu memberaction"]//a//strong//text()')).strip() + ' / ' + time
                item.set('sk', sk)
                author = textify(node.select('.//div[@class="popupmenu memberaction"]//a//strong//text()')).strip()
                item.set('author', repr(author))
                item.set('pc_experience', textify(node.select('.//span[contains(text(),"PC Experience:")]//parent::p/text()')))
                item.set('operating_system', textify(node.select('.//span[contains(text(),"Operating System:")]//parent::p/text()')))
                comment_title = textify(node.select('.//h2[@class="title icon"]/text()')).strip()
                item.set('comment_title', comment_title)
                comment = textify(node.select('.//blockquote[@class="postcontent restore "]')) or textify(node.select('.//blockquote[@class="postcontent restore"]'))
                item.set('comment', comment)
                image_url = textify(node.select('.//a[@class="postuseravatar"]//img/@src'))
                item.set('image_url', repr(image_url))
                author_title =  textify(node.select('.//span[@class="usertitle"]')).strip()
                item.set('author_title', author_title)
                item.set('title_image', textify(node.select('.//span[@class="usertitle"]//img/@src')))
                post_counter = textify(node.select('.//a[@class="postcounter"]'))
                post_counter = thread_title + post_counter
                item.set('post_counter', post_counter)
                key = []
                nodelist1 = node.select('.//dl[@class="userinfo_extra"]//dt')
                for cnode in nodelist1:
                    key.append(textify(cnode.select('./text()')))
                value = []
                nodelist2 = node.select('.//dl[@class="userinfo_extra"]//dd')
                for dnode in nodelist2:
                    value.append(textify(dnode.select('./text()')))
                author_details = {}
                for i in range(len(key)):
                    author_details[key[i]] = value[i]
                    item.set('author_details', author_details)
                yield item.process()

        if hdoc.select('//a[@rel="prev"]/@href'):
            prev_url = textify(hdoc.select('//a[@rel="prev"]/@href')).split('\n\n\n')
            prev_url = prev_url[0]

            yield Request(prev_url, self.parse_terminal_details, response, meta=response.meta)
