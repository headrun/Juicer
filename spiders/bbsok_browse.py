import re
import time

from dateutil import parser
from juicer.utils import *

class Bbsok(JuicerSpider):
    name = "bbsok"
    #start_urls = ['http://bbs.oksingapore.com/forum.php']
    start_urls = ['http://forum.oksingapore.com/']

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
            check_date = datetime.datetime.now() + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        urls = hdoc.select_urls(['//a[contains(@href,"forum.php?gid")]/@href'],response)
        for url in urls:
            yield Request(url, self.parse_sub, response)

    def parse_sub(self, response):
        hdoc = HTML(response)
        next_url = ""
        nodes = hdoc.select('//table[@class="fl_tb"]/tr')

        for node in nodes:
            post_time = textify(node.select('./td[@class="fl_by"]/div/cite/text()'))
            if post_time == "":
                post_time = textify(node.select('./td[@class="fl_by"]/div/cite/span/@title'))
            ps_time = parse_date(post_time, True)

            if ps_time > self.latest_dt:
                    forum_url = textify(node.select('.//td/h2/a/@href'))
                    forum_title = textify(node.select('.//td/h2/a/text()'))
                    next_url = textify(hdoc.select('//a[@class="nxt"]/@href'))
                    yield Request(forum_url, self.parse_forum, response, meta ={'forum_title':forum_title})
        if  next_url :
            yield Request(next_url, self.parse_sub, response)

    def parse_forum(self, response):
        hdoc = HTML(response)
        forum_title = response.meta['forum_title']
        terminal_link = ""
        nodes = hdoc.select('//table/tbody[contains(@id,"thread_")]/tr')
        next_url = ""
        for node in nodes:
            post_time = textify(node.select(".//td[@class='by']//em//span/@title"))
            if not post_time:
                post_time = textify(node.select('.//td[@class="by"]//em//a/text()'))
            ps_time = parse_date(post_time)
            if ps_time >= self.latest_dt :
                next_url = textify(hdoc.select('//a[@class="nxt"]/@href'))
                terminal_link = textify(node.select('.//th//span[@class="xst"]//a/@href[contains(string(),"thread-")]'))
                yield Request(terminal_link, self.parse_terminal, response, meta = {'url':response.url, 'forum_title': forum_title})

        if next_url:
            yield Request(next_url, self.parse_forum, response, meta = {'forum_title':response.meta['forum_title']})


    def parse_terminal(self, response):
        hdoc=HTML(response)

        nodes = hdoc.select('//div[@class="wp cl"]//div[@class= "pl"]/div')
        thread_id = ''.join(re.findall(r'thread-(\d.*).h', response.url))
        forum_id = ''.join(re.findall(r'forum-(\d.*).h', response.meta['url']))
        if not forum_id:
            forum_id = ''.join(re.findall(r'fid=(\d+)', response.meta['url']))
        thread_title = textify(hdoc.select('//h1[@class="ts"]//a//text()'))
        nextpage_url = textify(hdoc.select('//a[@class="nxt"]/@href'))

        for nod in nodes:
            item=Item(response)
            #forum Detail
            author = {}
            postedtime = textify(nod.select('.//div[@class="authi xg1"]//em[contains(@id,"authorpost")]/span/@title'))

            if not postedtime :
                postedtime = textify(nod.select('.//div[@class="authi xg1"]/em[contains(@id,"authorpost")]//text()'))
            if not postedtime:
                continue

            pstedtime = re.findall(r'\d\d\d\d-.*', postedtime)
            postedtime = parse_date(pstedtime[0])

            if postedtime < self.latest_dt:
               continue

            text = textify(nod.select('.//td[@class="t_f"]//text()'))
            if text != '':
                item.set("text",text)

                item.set('dt_added',postedtime)
                if self.flag:
                    self.update_dt(postedtime)

                try:
                    item.set('forum.id', forum_id)
                except Exception:
                    pass
                item.set('forum.url', response.meta['url'])
                item.set('forum.title' , response.meta['forum_title'])

                item.set('thread.id', thread_id)
                item.set('thread.title',thread_title)
                item.set('thread.url', response.url)
                item.set('title', thread_title)

                #Post Related Data
                user_name = textify(nod.select('.//table/tr//td[@class="pls"]//div[@class="authi"]/a[@class="xw1"]/text()'))
                if user_name == "":
                    continue
                item.set("author.name", user_name)
                a_url = textify(nod.select('.//table/tr//td[@class="pls"]//div[@class="authi"]/a[@class="xw1"]/@href'))
                a_id = re.findall(r'uid-(\d+)',a_url)
                item.set('author.id',str(a_id[0]))
                item.set('author.url',a_url)


                postedtime = textify(nod.select('.//div[@class="authi xg1"]/em[contains(@id,"authorpost")]/span/@title'))
                if postedtime == "":
                    postedtime = textify(nod.select('.//div[@class="authi xg1"]/em[contains(@id,"authorpost")]//text()'))
                postedtime = parse_date(postedtime, True)
                item.set('dt_added',postedtime)

                pid = textify(nod.select('.//div/@id[contains(string(), "post")]'))
                pid = re.findall(r'post_rate_div_(\d+)', pid)
                if not pid:
                    pid = textify(nod.select('.//table/@id'))
                    pid = re.findall(r'pid(\d+)', pid)

                item.set("sk",str(pid[0]))
                url ="#pid" + pid[0]
                url = urlparse.urljoin(response.url, url)
                item.set('url',url)
                #yield item.process()

                ob = pprint.PrettyPrinter(indent=2)
                ob.pprint(item.data)

        if nextpage_url:
            yield Request(nextpage_url, self.parse_terminal, response, meta={'url' : response.meta['url'], 'forum_title':response.meta['forum_title']})
