from juicer.utils import*
from dateutil import parser
from datetime import timedelta
from datetime import datetime


class Zaobao_premium(JuicerSpider):
    name = 'zaobao_premium'
    start_urls = ['http://www.zaobao.com.sg/premium']

    
    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@class, "jewel-premium-")]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.zaobao.com.sg' + cat
            yield Request(cat,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="ds-1col node node-article node-teaser view-mode-teaser post-item clearfix"]')
        for node in nodes:
            dt = textify(node.select('./span[@class="datestamp"]//text()'))
            date=str(datetime.strptime(dt, '%d/%m/%Y').strftime('%m/%d/%Y'))
            date_added = get_timestamp(parse_date(xcode(date)) - timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a[@data-path]/@href'))
            if 'http' not in link: link = 'http://www.zaobao.com.sg' + link
            if 'comic/stor' in link:
                continue
            yield Request(link,self.parse_details,response)
        if not nodes:
            add_cat = hdoc.select('//span[@class="more"]/a/@href').extract()
            for cat in add_cat:
                if 'http' not in cat: cat = 'http://www.zaobao.com.sg' + cat
                yield Request(cat,self.parse_links,response)

        nxt_pg = textify(hdoc.select('//li[@class="pager-next first last"]//a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.zaobao.com.sg' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="body-content"]//h1//text()'))
        dt = textify(hdoc.select('//aside//span[@class="datestamp"]//text()'))
        dt =  dt.replace(u'\u5e74','-').replace(u'\u6708','-')
        date = ''.join(re.findall('\d{4}-\d{1}-\d{2}', dt))
        if not date:
            date = ''.join(re.findall('\d{4}-\d{2}-\d{2}', dt)) or ''.join(re.findall('\d{4}-\d{1}-\d{1}', dt))
        dt_added = get_timestamp(parse_date(xcode(date)) - timedelta(hours=8))

        text = textify(hdoc.select('//div[@id="FineDining"]//text()')) or textify(hdoc.select('//div[@id="FineDining"]//p//text()')) or textify(hdoc.select('//div[@id="FineDining"]//li//text()')) or textify(hdoc.select('//div[@id="FineDining"]//p//following-sibling::text()')) or textify(hdoc.select('//div[@id="FineDining"]//span//text()'))


        junk_txt = textify(hdoc.select('//div[@id="dfp-ad-imu1"]//text()'))
        text = text.replace(junk_txt,'')
        author = textify(hdoc.select('//span[@class="contributor meta-byline"]//a//text()'))
        auth_url = textify(hdoc.select('//span[@class="contributor meta-byline"]//a//@href'))
        if 'http' not in auth_url: auth_url = 'http://www.zaobao.com.sg' + auth_url

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author'{'name':xcode(author)})
        item.set('author_url',xcode(auth_url))
        item.set('xtags',['news_sourcetype_manual','singapore_country_manual'])
        yield item.process()


