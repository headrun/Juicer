from juicer.utils import*
from dateutil import parser

class JfdailyCN(JuicerSpider):
    name = 'jfdaily'
    start_urls = ['http://www.jfdaily.com.cn/', 'http://www.jfdaily.com.cn/rexian/', 'http://www.jfdaily.com.cn/shendu/', 'http://www.jfdaily.com.cn/yexian/', 'http://www.jfdaily.com.cn/shouye/', 'http://www.jfdaily.com.cn/qushi/', 'http://newspaper.jfdaily.com/isdb/html/2016-05/26/node_2.htm', 'http://newspaper.jfdaily.com/shfzb/html/2016-05/25/node_2.htm', 'http://newspaper.jfdaily.com/jfrb/html/2016-05/26/node_2.htm', 'http://newspaper.jfdaily.com/xwcb/html/2016-05/26/node_2.htm', 'http://newspaper.jfdaily.com/sjfwdb/html/2016-05/25/node_2.htm']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav"]/li/a/@href').extract()
        for category in categories[:3]:
            if '#' in category:
                continue
            if 'http' not in category: category = 'http://www.jfdaily.com.cn' + category
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        cat_p = response.url.split('/')[-2]
        nodes = hdoc.select('//div[@class="image_info02"]')
        for node in nodes:
            date = textify(node.select('.//span//text()').extract())
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next =  False
                continue

            link = textify(node.select('./h2/a/@href'))
            yield Request(link,self.parse_data,response)

        if 'index_html' not in response.url:
            nxt_pg = textify(hdoc.select('//p[@class="paging"]//text()'))
            if nxt_pg:
                page = int(nxt_pg.split('(')[1].split(',')[0])
                page = page + 1
                for _page in range(1, page):
                    url = 'http://www.jfdaily.com.cn./%s/index_%s.html' %(cat_p, _page)
                    yield Request(url,self.parse_links,response)


    def parse_data(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="topNewslong"]//text()'))
        import pdb;pdb.set_trace()
