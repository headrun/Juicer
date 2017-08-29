import urllib
import datetime
import time
import re

from juicer.utils import *

class Cforum(JuicerSpider):
    name = "cforum"
    start_urls = ['http://cforum.cari.com.my/forum.php']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.cutoff_dt = None
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.flag = False

    def parse(self, response):
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

        nodes = hdoc.select("//div[contains(@id,'category_')]//table//tr//td")
        for nod in nodes:
            lastpost_dt = textify(nod.select(".//dd//a")).encode('utf8')
            if "\xe6\x9c\x80\xe5\x90\x8e\xe5\x8f\x91\xe8\xa1\xa8" in lastpost_dt:
                lastpost_dt = textify(nod.select(".//dd//a/text()"))
                lastpost_dt = re.findall(r':\s(\d.*\w)',lastpost_dt)
            if lastpost_dt :
                ln = lastpost_dt[0]
                try:
                    lastpost_dt = parse_date(ln, True)
                except Exception:
                    continue

                if not isinstance(lastpost_dt ,datetime.datetime):
                    continue
                if lastpost_dt > self.latest_dt :
                    link = textify(nod.select(".//div[@class='fl_icn_g']//a/@href"))
                    forum_title = textify(nod.select(".//div[@class='fl_icn_g']//a/text()"))
                    yield Request(link, self.parse_sub, response, meta = {"forum_title": forum_title})

    def parse_sub(self,response):
        hdoc = HTML(response)

        sub_forums = hdoc.select('//div[contains(@id,"subforum_")]//tr/td[@class="fl_by"]/parent::tr')
        for sub_forum in sub_forums:
            post_dt = textify(sub_forum.select('.//td[@class="fl_by"]//cite/text()'))
            post_dt = parse_date(post_dt, True)
            if post_dt >= self.latest_dt:
                url = textify(sub_forum.select('.//h2/a/@href'))
                yield Request(url, self.parse_sub, response)


        nodes = hdoc.select('//table//tbody[contains(@id,"thread_")]//tr')
        next_url = ""
        forum_title = textify(hdoc.select("//title/text()"))

        for nod in nodes:
            lastpost_dt = textify(nod.select('.//td[@class="by"]/em/a/text()'))
            lastpost_dt = parse_date(lastpost_dt, True)

            if lastpost_dt >= self.latest_dt:
                #if self.flag:
                self.update_dt(lastpost_dt)
                next_url = textify(hdoc.select('//a[@class="nxt"]/@href')).split(" ")
                next_url = urlparse.urljoin(response.url, next_url[0])
                link = textify(nod.select('.//th//a[contains(@href,"viewthread")]/@href')).split(" ")
                title = textify(nod.select('.//th//a[contains(@href,"viewthread") and @class="xst"]/text()'))
                yield Request(link[0], self.parse_post, response, meta={ 'url' :response.url, 'title' :title, "forum_title":forum_title})

        if next_url:
            yield Request(next_url, self.parse_sub, response)

    def parse_post(self,response):
        hdoc = HTML(response)

        forum_id = re.findall(r'fid=(\d+)', response.meta['url'])
        thread_id = re.findall(r'tid=(\d+)', response.url)
        nodes = hdoc.select("//div[@id='postlist']/div[contains(@id,'post_')]")
        nextpage_url = ""
        nextpage_url = textify(hdoc.select('//div[@class="pgs mbm cl "]//a[@class="nxt"]/@href'))

        for nod in nodes :
            item = Item(response)
            try:
                lastpost_dt = textify(nod.select('.//div[@class="authi"]//em/text()'))
                lastpost_dt = re.findall(r'\s(\d.*)', lastpost_dt)
                lastpost_dt = parse_date(lastpost_dt[0], True)
            except Exception:
                continue

            if lastpost_dt <= self.latest_dt :
                continue

            self.update_dt(lastpost_dt)

            item.set("dt_added", lastpost_dt)
            thread_title = response.meta['title']
            item.set("thread.title", thread_title)
            item.set('thread.id',thread_id[0])
            item.set('thread.url', response.url)

            forum_title =  response.meta['forum_title']
            if "Powered by Discuz" in forum_title:
                forum_title = (re.sub(r'Powered \w.*', " ", forum_title)).strip()
            item.set('forum.title', forum_title)
            item.set('forum.url', response.meta['url'])
            try:
                item.set('forum.id', forum_id[0])
            except IndexError:
                pass

            author_name = textify(nod.select('.//div[@class="authi"]//a[@class="xw1"]/text()'))
            item.set('author.name',author_name)
            author_url = textify(nod.select('.//div[@class="authi"]//a[@class="xw1"]/@href'))
            author_url = urlparse.urljoin(response.url,author_url)
            item.set('author.url',author_url)
            author_id = re.findall(r'uid=(\d+)',author_url)
            if author_id:
                item.set("author.id",author_id[0])
            else:
                pass

            url = textify(nod.select('.//div[@class="pi"]//a[contains(@id, "postnum")]/@href'))
            url = urlparse.urljoin(response.url,url)
            item.set('url', url)
            sk = textify(nod.select(".//table/@id"))
            sk = re.findall(r'pid(\d+)', sk)
            item.set('sk', str(sk[0]))
            title = response.meta['title']
            item.set("title",title)
            lists = nod.select(".//dl[@class='pil cl']//dt")
            for li in lists:
                txt = textify(li.select(".//text()")).encode('utf8')
                if txt == "\xe6\xb3\xa8\xe5\x86\x8c\xe6\x97\xb6\xe9\x97\xb4":
                    joined_dt = textify(li.select("./following-sibling::dd[1]/text()"))
                    joined_dt = parse_date(joined_dt,True)
                    item.set('author.join_dt',joined_dt)
            text = textify(nod.select(".//td[@class='t_f']//text()"))
            item.set("text",text)
            yield item.process()

        if nextpage_url:
            yield Request(nextpage_url, self.parse_post, response,meta={ 'url' :response.meta['url'], 'title' :response.meta['title'], "forum_title": response.meta['forum_title']})
