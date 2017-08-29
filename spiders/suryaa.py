from juicer.utils import*
from dateutil import parser

class SuryaaNews(JuicerSpider):
    name = "suryaa_news"
    start_urls = ['http://www.suryaa.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categores = hdoc.select('//ul[@class="nav navbar-nav"]//li/a/@href').extract()
        for cat in categores:
            if 'index.html' in cat or 'epaper.suryaa.com' in cat:
                continue
            if 'http' not in cat: cat = 'http://www.suryaa.com/' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        add_cate = hdoc.select('//ul[@class="dropdown-menu"]//a[2]/@href').extract()
        for cate in add_cate:
            if 'http' not in cate: 
                domain = ''.join(re.findall('.*.com/', response.url))
                cate = domain+cate
            yield Request(cate,self.parse_main_links,response)
        if not add_cate:
            is_nxt = True
            nodes = hdoc.select('//div[@class="media-body"]')
            for node in nodes:
                date = textify(node.select('.//div[@class="comments_box"]//text()'))
                date = date.replace('Updated:','')
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
                if date_added < get_current_timestamp()-86000*30:
                    is_nxt = False
                    continue
                link = textify(node.select('./strong/a/@href'))
                if 'http' not in link:
                    domain = ''.join(re.findall('.*.com/', response.url))
                    link = domain+link
                yield Request(link,self.parse_details,response)
            nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//li//a[strong[contains(text(), "Next")]]/@href'))
            if 'http' not in nxt_pg:
                domain = ''.join(re.findall('.*.com/', response.url))
                nxt_pg = domain+ nxt_pg
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_links,response)

        aadd_links = hdoc.select('//ul[@class="labels_nav"]//li/a/@href').extract()
        for lin in  aadd_links:
            yield Request(lin,self.parse_sub_link,response)

    def parse_main_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="media-body"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="comments_box"]//text()')) or textify(node.select('.//span//a[@title]/text()'))
            date = date.replace('Updated:','')
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86000*30:
                is_nxt = False
                continue
            link = textify(node.select('./strong/a/@href')) or textify(node.select('./a/@href'))
            if 'http' not in link:
                domain = ''.join(re.findall('.*.com/', response.url))
                link = domain+link
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//li//a[strong[contains(text(), "Next")]]/@href'))
        if 'http' not in nxt_pg:
            domain = ''.join(re.findall('.*.com/', response.url))
            nxt_pg = domain+ nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_main_links,response)

    def parse_sub_link(self,response):
        hdoc = HTML(response)
        sub_links = hdoc.select('//div[@align="right"]/a/@href').extract()
        for lin in sub_links:
            if 'http' not in lin:
                domain = ''.join(re.findall('.*.com/', response.url))
                lin = domain + lin
            yield Request(lin,self.parse_main_links,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="col-lg-8 col-md-8"]//h1//strong//text()'))
        text = textify(hdoc.select('//div[@class="col-md-12"]//p//text()')) or textify(hdoc.select('//div[@class="single_page_content"]//p//text()')) or textify(hdoc.select('//div[@class="single_page_content"]//span[not(script)]//text()')) or textify(hdoc.select('//div[@class="col-md-12"]//span//text()'))
        date = textify(hdoc.select('//div[@class="col-lg-8 col-md-8"]//span[contains(text(), "Updated:")]/following-sibling::a//text()')) or textify(hdoc.select('//div[@class="col-lg-8 col-md-8"]//span[contains(text(), "Written by")]/following-sibling::a//text()')) or textify(hdoc.select('//span[@class="meta_date"]//a/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//div[@class="col-lg-8 col-md-8"]//span[contains(text(), "ritten")]//text()')) or textify(hdoc.select('//div[@class="col-lg-8 col-md-8"]//span[contains(text(), "Updated:")]')) or textify(hdoc.select('//div[contains(@class, "collapse navbar-collapse")]//following-sibling::span[contains(text(), "ritten")]//text()'))
        author = author.replace('Written by :','').replace('| Updated:','')


        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield  item.process()














