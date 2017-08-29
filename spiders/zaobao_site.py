from juicer.utils import *

class Zaobao_Site(JuicerSpider):
    name = "zaobao_site"
    start_urls = "http://realtime.zaobao.com.sg/"

    def parse(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//table/tr/td[@class="cont"]/li')
        offset = datetime.timedelta(hours=8)

        for node in nodes:
            posted_time = textify(node.select('.//a/text()'))
            posted_time = re.findall(r'\d\d',posted_time)
            posted_time = posted_time[0] + ":" + posted_time[1] + ":" + "00"
            posted_time = parse_date(posted_time)
            self.update_dt(posted_time,offset)
            link = textify(node.select(".//a/@href"))
            yield Request(link, self.parse_terminal, response)

    def parse_terminal(self,response):
        hdoc = HTML(response)
        item = Item(response)

        item.set('url', response.url)
        item.textify('title', "//p[@class='title']/text()")
        times =  textify(hdoc.select('//p[@class="small"]/text()'))
        time  = re.findall(r'(\d.*-\d+)', times)
        time = parse_date(time[0])
        item.set('dt_added',time)
        text = textify(hdoc.select('//p[not(@class="title") and not(@class="small")]/text()'))
        item.set("text", text)
        yield item.process()
