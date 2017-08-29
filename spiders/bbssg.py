import datetime

from dateutil import parser
from juicer.utils import *

class Bbssg(JuicerSpider):
    name = "bbssg"
    start_urls = "http://bbs.sgchinese.net/"

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.cutoff_dt = None 

    def parse(self,response):
        hdoc = HTML(response)

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select('//div[contains(@id, "category_")]/table//tr')
        nodes1 = hdoc.select('//table/tbody[contains(@id,"thread")]')

        for node in nodes:
            post_time =  textify(node.select('.//cite/span/@title'))
            post_time = parse_date(post_time)

            if post_time >= self.cutoff_dt:
                link = textify(node.select('.//td/h2/a/@href'))
                title = textify(hdoc.select('//title'))

                if "forum" in link and link:
                    yield Request(link, self.parse, response)
                elif "thread"in link:
                    yield Request(link, self.parse_post, response, meta={'url':response.url,'title':title})


        for node in nodes:
            post_time = textify(node.select('.//td//span/@title')).split(" ")

            if len(post_time) > 2:
                post_time = " ".join(post_time[-2:])
                post_time = parse_date(post_time)
            else :
                continue
            if post_time >= self.cutoff_dt:
                link = textify(node.select('.//td[class="fl_g"]//dl/dt/a/@href'))
                title = textify(hdoc.select('//title'))

                if "forum" in link:
                    yield Request(link ,self.parse, response)
                elif "thread" in link:
                    yield Request(link, self.parse_post, response, meta={'url':response.url,'title':title})


        for  node in nodes1:
            post_time = textify(node.select('.//td[@class="by"]//span/@title')).split(" ")

            if post_time :
                pt_time = parse_date(post_time[0])

            if pt_time >= self.cutoff_dt:
                link = textify(node.select('.//th//a[@class="xst"]/@href'))
                title = textify(hdoc.select('//title'))

                if "thread" in link:
                    yield Request(link, self.parse_post, response,  meta={'url':response.url,'title':title})
                else:
                    yield Request(link, self.parse, response)



    def parse_post(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div//table[contains(@id, "pid")]')

        forum_id = re.findall(r'forum-(\d.*).h', response.meta['url'])
        thread_id = re.findall(r'thread-(\d.*).h', response.url)
        thread_title = textify(hdoc.select('//title'))



        for nod in nodes:
            item = Item(response)
            author = {}
            post_dt = textify(nod.select('.//div[@class="authi"]//span/@title'))
            post_dt = parse_date(post_dt)
            if post_dt < self.cutoff_dt:
                continue
            item.set("dt_added",post_dt)
            #forum details
            try:
                item.set("forum.id", str(forum_id[0]))
            except Exception:
                pass
            item.set("forum.url", response.meta['url'])
            item.set("forum.title", response.meta['title'])

            #Thread details
            item.set("thread.id", str(thread_id[0]))
            item.set("thread.url", response.url)
            item.set("thread.title", thread_title)

            item.textify('title',"//title")

            url = textify(nod.select('.//a[contains(@id,"postnum")]/@href'))
            item.set('url',url)
            pid = textify(nod.select('./@id'))
            pid = re.findall(r'pid(\d.*)',pid)
            item.set('sk',str(pid[0]))

            author_name = textify(nod.select('.//div[@class="pi"]//div[@class ="authi"]/a[@class="xw1"]'))
            item.set('author.name',author_name)
            url = textify(nod.select('.//div[@class="pi"]//div[@class ="authi"]/a[@class="xw1"]/@href'))
            item.set("author.url",url)
            uid = re.findall(r'uid-(\d*)',url)
            item.set('author.id',str(uid[0]))
            post_time = textify('.//div/div[@class="authi"]//a[@class="xw1"]/text()')
            post_time = re.findall(r'(\d-.*)',post_time)
            if post_time :
                post_time = post_time[0]
            post_time = textify(nod.select('.//div[@class="authi"]//span/@title'))
            post_time = parse_date(post_time)
            self.update_dt(post_time)

            text = textify(nod.select('.//td[contains(@id,"postmessage")]'))
            item.set('text',text)
            #joined_date = textify(nod.select('.//dl[contains(@class,"pil")]//dt[contains(string(),"\xe6\xb3\xa8\xe5\x86\x8c\xe6\x97\xb6\xe9\x97\xb4")]/following-sibling::dd[1]'))
            lists = nod.select('.//dl[contains(@class,"pil")]//dt')
            for li in lists:
                txt = textify(li.select('.//text()')).encode('utf8')
                if txt == "\xe6\xb3\xa8\xe5\x86\x8c\xe6\x97\xb6\xe9\x97\xb4":
                    joined_date = textify(li.select('./following-sibling::dd[1]'))
                    joined_date = parse_date(joined_date)
                    item.set('author.dt_joined',joined_date)

                elif txt == "\xe5\xb8\x96\xe5\xad\x90" :
                    posts = textify(li.select('.//following-sibling::dd[1]'))
                    print "post"
                    author["posts"] = int(posts)
                    item.set("author.num",author)


            yield item.process()
