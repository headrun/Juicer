from juicer.utils import*
from dateutil import parser

class MoneycontrolIN(JuicerSpider):
    name = 'moneycontrol_mod'
    start_urls = ['http://www.moneycontrol.com/news/']    

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="stickysub db  actlink "]/ul[@class="headbotmmenus1"]//li/a[@title]/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//li[contains(@id, "newslist-")]')
        for node in nodes:
            date = textify(node.select('.//span//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//h2/a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="pagenation"]//a[@class="act"]/following-sibling::a/@href').extract()[0])
        if 'http' not in nxt_pg: nxt_pg = 'http://www.moneycontrol.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//article[@class="article_box"]//h1//text()')) or textify(hdoc.select('//div[@class="arttidate"]//following-sibling::h1//text()'))
        dt = textify(hdoc.select('//div[@class="arttidate"]//text()'))
        date = ''.join(re.findall('(.*) \|',dt))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        add_txt = textify(hdoc.select('//h2[@class="subhead"]//text()'))
        junk_txt1 = textify(hdoc.select('//div[@class="FL MR30 wd225"]//text()'))
        junk_txt2 = textify(hdoc.select('//div[@class="ads-320-250 show-moblie mid-arti-ad"]//text()'))
        junk_txt3 = textify(hdoc.select('//div[@class="hide-moblie mid-arti-ad"]//text()'))
        junk_txt4 = textify(hdoc.select('//div[@class="clearfix"]//text()'))
        junk_txt5 = textify(hdoc.select('//div[@id="Moneycontrol_Mobile_WAP/MC_WAP_News/MC_WAP_News_Internal_300x250_Middle"]//text()'))
        text = textify(hdoc.select('//div[@class="arti-flow clearfix"]//text()')) or textify(hdoc.select('//div[contains(@class, "arti-flow")]//text()'))
        text = text.replace(junk_txt1,'').replace(junk_txt2,'').replace(junk_txt3,'').replace('Watch videos for more','')
        text = text.replace(junk_txt4,'').replace('Read More','').replace('For all recommendations report, click here','').replace(junk_txt5,'')
        text = add_txt + ' ' + text
        author = textify(hdoc.select('//div[@class="interviewee"]//text()')) or textify(hdoc.select('//span[@class="bybold"]//text()')) or textify(hdoc.select('//div[contains(@class, "arti-flow")]/strong[1]/text()'))
        author_url = textify(hdoc.select('//a[div[@class="interviewee"]]/@href'))

        
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()
        
