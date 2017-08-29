import re
import datetime

from dateutil import parser
from juicer.utils import *


class Zaobao(JuicerSpider):
    start_urls = ["http://luntan.zaobao.com/"]
    name = "zaobao_browse"

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.cutoff_dt = None 

    def parse(self, response):
        hdoc = HTML(response)
        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select("//div[@class='maintable']/div/div[@class='spaceborder spacebottom']/table/tbody[    @id='category_28']/tr[@class='row']")

        for node in nodes:
            lastpost_dt = textify(node.select('./td[@align="center"]/span[@class="smalltxt"]/a/text()'))
            lastpost_dt = parser.parse(lastpost_dt)

            if self.cutoff_dt >= lastpost_dt:
                continue

            url = textify(node.select('./td[@class="subject"]/a/@href'))
            yield Request(url, self.parse_sub, response)

    def parse_sub(self, response):
        hdoc = HTML(response)
        nodes1 = hdoc.select('//div[@class="maintable"]/div[@class="spaceborder"]/table')

        for node1 in nodes1:
            topic_dt = textify(node1.select(".//td[@class='f_last']/span/a/text()"))
            lastpost_dt = parser.parse(topic_dt)
            title = textify(hdoc.select("//title"))

            if lastpost_dt > self.cutoff_dt:
                url = textify(node1.select(".//td[@class='f_title']/a/@href"))
                yield Request(url, self.parse_terminal, response,meta={'url':response.url, 'title':title})

        # finding next page link and navigating there
        nodes = hdoc.select("//a[@class='p_redirect']")
        next_url = None

        for node in nodes:
            node_text = textify(node).encode('utf8')
            if node_text == "\xe2\x80\xba\xe2\x80\xba":
                next_url = node.select(".//@href").extract()[0]
                break

        yield Request(next_url, self.parse_sub, response)

    def parse_terminal(self, response):
        hdoc=HTML(response)
        title = textify(hdoc.select("//title"))

        nodes = hdoc.select("//form/div[@class='spaceborder']/table")
        for node in nodes:
            item = Item(response)
            author = {}

            posted_time = textify(node.select(".//tr/td/div/div/text()[1]"))
            posted_time = re.findall(r'(\s\d.*\d)', posted_time)
            posted_time = parse_date(posted_time[0])
            if posted_time < self.cutoff_dt:
                continue

            tid = re.findall(r'tid=(\d+\d)', response.url)
            item.set("thread.id", str(tid[0]))
            item.set("thread.title", title)
            thread_url = response.url
            if "redirect.php" in thread_url:
                thread_url = re.sub(r'(%20\w.*)', " ", thread_url)

            item.set("thread.url", thread_url)

            fid = re.findall(r'fid=(\d+)', response.meta['url'])
            item.set('forum.id', str(fid[0]))
            item.set('forum.url', response.meta['url'])
            item.set('forum.title', response.meta['title'])

            posted_time = textify(node.select(".//tr/td/div/div/text()[1]"))
            posted_time = re.findall(r'(\s\d.*\d)', posted_time)
            posted_time = parse_date(posted_time[0])
            item.set('dt_added', posted_time)

            url = textify(node.select('.//div[contains(@class,"right t_number")]/a/@onclick'))
            url = re.findall(r'(http:.*pid\d+)', url)
            item.set('url', url[0])
            sk = re.findall(r'pid(\d+\d)', url[0])
            item.set("sk", str(sk[0]))

            item.set("title", title)
            name = textify(node.select('.//td[@class="t_user"]/a[@target="_blank"]/text()'))
            author_url = textify(node.select('.//td[@class="t_user"]/a[@target="_blank"]/@href'))
            author_id = re.findall(r'uid=(\d+)', author_url)

            item.set("author.id", str(author_id[0]))
            item.set("author.name", name)
            author_url = urlparse.urljoin(response.url, author_url)
            item.set("author.url",author_url)
            #joined_dt = textify(node.select(".//div[@class='smalltxt']/text()[contains(string(),'\xe6\xb3\xa8\xe5\x86\x8c')]"))
            lists = node.select(".//div[@class='smalltxt']")
            for li in lists:
                txt = textify(li.select('.//text()')).encode('utf8')
                if "\xe6\xb3\xa8\xe5\x86\x8c" in txt:
                    posts= re.findall(r'\xe5\xb8\x96\xe5\xad\x90\s(\d+)',txt)
                    author['posts'] = int(posts[0])
                    joined_dt = re.findall(r'\xe6\xb3\xa8\xe5\x86\x8c\s(\d+)', txt)
                    joined_dt = parse_date(joined_dt[0])
                    item.set("author.dt_joined",joined_dt)

            item.set("author.num",author)
            text = textify(node.select('.//tr[2]/td/div/div/div/div'))
            item.set('text', text)

            yield item.process()
