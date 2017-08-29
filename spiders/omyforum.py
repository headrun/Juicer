import re
import sys
import datetime

from juicer.utils import *

RE_SESSION_REPLACE = re.compile(r's=\w+&')

class OmyBrowse(JuicerSpider):
    name = "omyforum"
    start_urls = ["http://forum.omy.sg/forumdisplay.php?f=1"]

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False

    def parse(self,response):
        hdoc = HTML(response)

        if self.latest_dt is None:
            latest = datetime.datetime.now() + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days= 7)
            self.latest_dt = latest - oneweek_diff
            self.flag = True

        if self.cutoff_dt is None:
            #check_date = self._latest_dt + datetime.timedelta(hours=8)
            check_date = datetime.datetime.now() + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select("//table/tbody/tr")

        for node in nodes:
            lastpost_dt = textify(node.select('.//div[@align="right"]/text()'))
            lastpost_dt = parse_date(lastpost_dt)
            link = textify(node.select('.//td[contains(@class,"alt")]/div[not(contains(@class,"small"))]\
                                        /a[contains(@href,"forumdisplay.php")]/@href'))

            if not link:
                continue

            if lastpost_dt > self.cutoff_dt:
                link = RE_SESSION_REPLACE.sub("", link)
                yield Request(link, self.parse_sub, response)

    def parse_sub(self, response):
        hdoc = HTML(response)
        nodes1 = hdoc.select("//td[@class='thead'][contains(string(),'Forum')]/ancestor::table//tr")
        nodes1 = []
        nodes2 = hdoc.select("//td[@class='thead'][contains(string(),'Thread')]/ancestor::table//tr")

        should_paginate = False
        for node1 in nodes1:
            forum_link = textify(node1.select('.//a[contains(@href,"forumdisplay.php")]/@href'))
            forum_title = textify(node1.select('.//a[contains(@href,"forumdisplay.php")]//text()'))

            if not forum_link:
                continue

            lastpost_dt = textify(node1.select('.//div[@class="smallfont"]//span[@class="time"]/text()|\
                                                .//div[@class="smallfont"]//span[@class="time"]/parent::div/text()'))
            lastpost_dt = lastpost_dt.replace('by','').strip()
            lastpost_dt = parse_date(lastpost_dt)
            title = textify(hdoc.select("//title/text()"))

            if lastpost_dt >= self.latest_dt:

                if "forumdisplay" in forum_link:
                    forum_link = RE_SESSION_REPLACE.sub("", forum_link)
                    yield Request(forum_link, self.parse_sub, response)

        for nod in nodes2 :
            thread_link = textify(nod.select('.//td[@class="alt1"][contains(@id,"td_threadtitle_")]//span[@class="smallfont"]//a[contains(text(),"Last Page")]/@href'))
            lastpage = True
            forum_title = textify(hdoc.select("//title/text()"))

            if not thread_link :
                thread_link = textify(nod.select('.//td[contains(@id,"td_threadtitle_")]/div//a[contains(@id,"thread_title_")]/@href'))
                lastpage = False
            thread_title = textify(nod.select('.//td[contains(@id,"td_threadtitle_")]/div//a[contains(@id,"thread_title_")]/text()'))


            if not thread_title:
                continue

            lastpost_dt = textify(nod.select('.//div[@class="smallfont"]//text()'))
            lastpost_dt = re.findall(r'\s(\d\d.*\d.*M)', lastpost_dt)

            if not lastpost_dt:
                continue

            ltpost_dt = parse_date(lastpost_dt[0])
            next_url = textify(hdoc.select('//a[contains(@title,"Next Page")]/@href')).split(" ")

            if ltpost_dt and ltpost_dt >= self.latest_dt:

                if self.flag:
                    self.update_dt(ltpost_dt)

                should_paginate = True
                thread_link = RE_SESSION_REPLACE.sub("", thread_link)
                yield Request(thread_link, self.parse_posts, response, meta = { 'url' : response.url, 'title' : thread_title, 'forum_title':forum_title,'last':lastpage})


        if should_paginate and next_url:
            next_url = RE_SESSION_REPLACE.sub("", next_url[0])
            yield Request(next_url, self.parse_sub, response)

    def parse_posts(self, response):
        hdoc = HTML(response)
        author = {}
        nodes = hdoc.select('//div[@id="posts"]/div[contains(@id,"edit")]')
        forum_url = response.meta['url']
        forum_title = (re.sub(r'omy Forum -', " ", response.meta['forum_title'])).strip()
        forum_id = re.findall(r'f=(\d+)',response.meta['url'])
        prev_link = ""
        next_link = ""
        for node in nodes:
            tm = textify(node.select('.//table[@class="tborder"]/tr/td[@class="thead"]/text()'))
            if tm and tm != "#":
                time1 = re.sub('#', " ", tm)
                up_time = parse_date(time1)

            if response.meta['last'] and up_time > self.latest_dt :
                prev_link = textify(hdoc.select('//a[contains(@title,"Prev Page")]/@href')).split(" ")
            else:
                next_link = textify(hdoc.select('//div[@class="pagenav"]//table//td[@class="alt1"]//a/@href'))
                pass

            if not up_time >= self.latest_dt:
                continue
            item = Item(response, node=node)

            item.set('title', response.meta['title'])

            post_url = textify(node.select('.//a[contains(@href,"showpost")]/@href'))
            sk = re.findall(r'p=(\d.*)&',post_url)
            item.set("sk", str(sk[0]))

            item.set('thread.id', re.findall(r't=(\d+\d)', response.url)[0])
            item.set('thread.url', RE_SESSION_REPLACE.sub("", response.url))
            item.set('thread.title', response.meta['title'])

            item.set('forum.url', response.meta['url'])
            if forum_id:
                item.set('forum.id', forum_id[0])
            item.set('forum.title', forum_title)

            item.set('dt_added', up_time)
            item.textify("author.name", './/table[@class="tborder"]//div/a[@class="bigusername"]')
            user_link = textify(node.select('.//table[@class="tborder"]//div/a[@class="bigusername"]/@href'))
            user_link = urlparse.urljoin('http://forum.omy.sg/', user_link)
            item.set("author.url", RE_SESSION_REPLACE.sub("", user_link))

            ps_url = urlparse.urljoin('http://forum.omy.sg/', post_url)
            ps_url = RE_SESSION_REPLACE.sub("", ps_url)
            item.set("url", ps_url)

            au_id = re.findall(r'u=(\d.*)', user_link)
            item.set("author.id", ''.join(au_id[0]))

            joined = textify(node.select('.//td[@class="alt2"]/div[@class="smallfont"]/div/text()[contains(string(), "Date")]')).split(" ")[-1:]
            j_dt = parse_date(joined[0]) + datetime.timedelta(hours=8)
            item.set("author.join_dt", j_dt)

            post = textify(node.select('.//td[@class="alt2"]/div[@class="smallfont"]/div/text()[contains(string(), "Posts")]')).split(" ")[-1:]
            author["posts"] = int(post[0].replace(',', ''))
            item.set("author.num", author)

            item.textify('text', ".//div[contains(@id,'post_message_')]")

            yield item.process()

        if response.meta['last']:
            if prev_link:
                last = True
                prev_link = RE_SESSION_REPLACE.sub("",prev_link[0])
                yield Request(prev_link, self.parse_posts, response, meta={'url': forum_url, 'title': response.meta['title'], 'forum_title': response.meta['forum_title'],'last':last})
        else:
            if next_link:
                last = False
                next_link = next_link.split(" ")
                yield Request(next_link[0], self.parse_posts, response, meta={'url': forum_url, 'title': response.meta['title'], 'forum_title': response.meta['forum_title'],'last':last})
