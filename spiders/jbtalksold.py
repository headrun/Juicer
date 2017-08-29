from juicer.utils import *
from dateutil import parser

class JbTalks(JuicerSpider):
    name = "jbtalks1"
    start_urls = ['http://www.jbtalks.cc/index.php']

    def __init__(self, *args, **kwargs):
         JuicerSpider.__init__(self, *args, **kwargs)
         self.cutoff_dt = None

    def parse(self, response):
        hdoc = HTML(response)
        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff
        next_url = ""

        node_type1 = hdoc.select('//table[contains(@id,"category_")]//tbody[(contains(@id,"forum"))]//tr')
        node_type2 = hdoc.select('//table[contains(@id,"category_")]//tbody[not(contains(@id,"forum"))]//tr//th')
        node_type3 = hdoc.select('//div[@id="subforum"]/table/tbody/tr')
        node_type4 = hdoc.select("//table[@class='datatable']/tbody")

        title = textify(hdoc.select('//title'))

        for node in node_type1:
             lastpost_dt = textify(node.select('.//td[contains(@class,"last")]//cite/text()'))
             lastpost_dt = parse_date(lastpost_dt)

             if lastpost_dt >= self.cutoff_dt and lastpost_dt:
                link = textify(node.select('.//h2//a[contains(@href,"forum-")]/@href'))
                if "thread-" in link:
                    yield Request(link, self.parse_thread, response, meta={'url': response.url, 'title': title})
                elif "forum" in link:
                    yield Request(link, self.parse, response)

        #TYPE 2
        for node in node_type2:
            lastpost_dt = textify(node.select('.//p//a[contains(@href,"redirect.php")]/text()'))

            if lastpost_dt == '' :
               continue
            lastpost_dt = parse_date(lastpost_dt)
            if lastpost_dt >= self.cutoff_dt and lastpost_dt:
                link = textify(node.select('.//a[contains(@href,"forum-")]/@href'))
                if "thread-" in link:
                    yield Request(link, self.parse_thread, response, meta={'url': response.url,'title': title})
                elif "forum" in link:
                    yield Request(link, self.parse, response)


        for node in node_type3:
            lastpost_dt = textify(node.select('.//td[contains(@class,"last")]//cite/text()'))
            if not lastpost_dt:
                continue

            lastpost_dt = parse_date(lastpost_dt)
            if lastpost_dt >= self.cutoff_dt:
                link = textify(node.select('.//h2/a/@href'))
                if "thread-" in link:
                   yield Request(link, self.parse_thread, response, meta={'url': response.url,'title': title})
                elif "forum" in link:
                    yield Request(link, self.parse, response)

        for node in node_type4:
            lastpost_dt = textify(node.select(".//td[contains(@class,'lastpost')]/em/a/text()"))
            lastpost_dt = parse_date(lastpost_dt)

            if lastpost_dt >= self.cutoff_dt:
                link = textify(node.select(".//span[contains(@id,'thread')]/a[contains(@href,'thread')]/@href"))
                yield Request(link, self.parse_thread, response, meta={'url': response.url, 'title': title})

                if not lastpost_dt < self.cutoff_dt and next_url:
                    next_url = textify(hdoc.select('//a[@class="next"]/@href'))[-1:]
                    yield Request(next_url, self.parse, response)

    def parse_thread(self,response):
        hdoc = HTML(response)

        forum_id = re.findall(r'forum-(.*).h', response.meta['url'])
        thread_id = re.findall(r'thread-(.*).h', response.url)
        title = textify(hdoc.select('//title'))

        nodes = hdoc.select("//div[contains(@id,'post_')]/table")
        for node in nodes:
                author = {}
                item = Item(response)
                item.set('title', title)

                #forum details
                posted_date = textify(node.select('.//em[contains(@id,"authorposton")]'))
                posted_date = re.findall(r'\s(\d.*)', posted_date)

                if not posted_date:
                    continue

                posted_date = parse_date(str(posted_date[0]))

                if posted_date < self.cutoff_dt:
                    continue

                tid = textify(node.select('.//div[@class="postact s_clear"]//a/@href[contains(string(),"pid")]'))
                sk = re.findall(r'pid=(\d+)', tid)
                item.set("sk", str(sk[0]))
                url = textify(node.select('.//div[@class="authorinfo"]//a/@href[contains(string(),"author")]'))
                url = "#pid"+str(sk[0])
                url = urlparse.urljoin(response.url,url)
                item.set('url', url)

                item.set('forum.id', str(forum_id[0]))
                item.set('forum.url', response.meta['url'])
                item.set('forum.name', response.meta['title'])

                #thread details
                item.set('thread.id', str(thread_id[0]))
                item.set('thread.url', response.url)
                item.set('thread.name', title)

                time = textify(node.select('.//div[@class="authorinfo"]/em')).split(" ")
                tm = " ".join(time[1:3])
                time1 = parser.parse(tm) + datetime.timedelta(hours=8)
                self.update_dt(time1)
                item.set("dt_added",time1)

                # ****************#
                authorurl = textify(node.select(".//div[@class='postinfo']/a/@href"))
                authorurl = urlparse.urljoin(response.url, authorurl)

                author_name = textify(node.select(".//div[@class='postinfo']/a/text()"))
                item.set('author.name',author_name)
                item.set('author.url', authorurl)
                user_url = textify (node.select(".//div[@class='postinfo']/a/@href"))
                user_id = re.findall(r'uid=(\d.*)', user_url)
                item.set('author.id', str(user_id[0]))

                #number_of_post = textify(node.select('.//dl[@class="profile s_clear"]//dt[contains(string(),"\xe5\xb8\x96\xe5\xad\x90")]/following-sibling::dd[1]/text()'))
                lists = node.select('.//dl[@class="profile s_clear"]//dt')
                for li in lists:
                    txt = textify(li.select('.//text()')).encode('utf8')
                    if txt == "\xe5\xb8\x96\xe5\xad\x90":
                        number_of_post = textify(li.select('.//following-sibling::dd[1]/text()'))
                        author["posts"] = int(number_of_post)
                        item.set("author.num", author)

                    elif txt == "\xe6\xb3\xa8\xe5\x86\x8c\xe6\x97\xb6\xe9\x97\xb4":
                        joined_date = textify(li.select('.//following-sibling::dd[1]/text()'))
                        joined_date = parser.parse(joined_date) + datetime.timedelta(hours=8)
                        item.set("author.join_dt", joined_date)
                item.textify('text', ".//td[contains(@id,'postmessage_')]")
                yield item.process()
