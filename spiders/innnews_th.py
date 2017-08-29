from juicer.utils import*
from dateutil import parser

class Innnews_Th(JuicerSpider):
    name = 'innnews_th'
    start_urls = ['http://www.innnews.co.th/shownews/breakingnews?category=0']

    def parse(self,response):
        hdoc =  HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="list-row"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="list-row-date"]//text()'))
            if u'\u0e21\u0e35.\u0e04' in date  or u'\u0e01.\u0e1e' in date or u'\u0e21.\u0e04' in date or u'\u0e18.\u0e04' in date or u'\u0e1e.\u0e22' in date or u'\u0e15.\u0e04' in date or u'\u0e01.\u0e22' in date or u'\u0e2a.\u0e04' in date or u'\u0e01.\u0e04' in date or u'\u0e21\u0e34.\u0e22' in date or '\u0e1e.\u0e04' in date or u'\u0e40\u0e21.\u0e22' in date: 


                date = date.replace(u'\u0e21\u0e35.\u0e04','March').replace(u'\u0e01.\u0e1e','Feb').replace(u'\u0e21.\u0e04','Jan').replace(u'\u0e18.\u0e04','Dec').replace(u'\u0e1e.\u0e22','Nov').replace(u'\u0e15.\u0e04','Oct').replace(u'\u0e01.\u0e22','Sep').replace(u'\u0e2a.\u0e04','Aug').replace(u'\u0e01.\u0e04','July').replace(u'\u0e21\u0e34.\u0e22','June').replace('\u0e1e.\u0e04','May').replace(u'\u0e40\u0e21.\u0e22','April')
                _date = ''.join(date.split('.')[0])
            date_added = get_timestamp(parse_date(xcode(_date)) -  datetime.timedelta(hours=7))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//a[@title]/@href'))
            if 'http' not in link: link = 'http://www.innnews.co.th/' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="yiiPager"]//li[@class="next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.innnews.co.th' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[contains(@class, "news-detail-title")]//text()')) or textify(hdoc.select('//div[contains(@class, "news-title")]//text()'))
        text = textify(hdoc.select('//div[@class="news-detail-detail"]//text()'))or textify(hdoc.select('//div[contains(@class, "news-detail")]//text()'))
        text = text.replace('Tweet','')
        ext_txt = textify(hdoc.select('//div[contains(@class, "news-brief")]//text()'))
        main_txt = ext_txt + '' + text
        date = textify(hdoc.select('//span[@class="news-detail-tag2"]//text()')) or textify(hdoc.select('//div[@class="det-news-time"]/a/following-sibling::text()'))
        
        if u'\u0e21\u0e35\u0e19\u0e32\u0e04\u0e21 \u0e1e.\u0e28' in date or u'\u0e19.' in date  or u'\u0e01\u0e38\u0e21\u0e20\u0e32\u0e1e\u0e31\u0e19\u0e18\u0e4c \u0e1e.\u0e28' in date or u'\u0e21\u0e01\u0e23\u0e32\u0e04\u0e21 \u0e1e.\u0e28' in date or u'\u0e18\u0e31\u0e19\u0e27\u0e32\u0e04\u0e21 \u0e1e.\u0e28' in date  or u'\u0e1e\u0e24\u0e28\u0e08\u0e34\u0e01\u0e32\u0e22\u0e19 \u0e1e.\u0e28' in date or u'\u0e15\u0e38\u0e25\u0e32\u0e04\u0e21 \u0e1e.\u0e28' in date or u'\u0e01\u0e31\u0e19\u0e22\u0e32\u0e22\u0e19 \u0e1e.\u0e28' in date or u'\u0e2a\u0e34\u0e07\u0e2b\u0e32\u0e04\u0e21 \u0e1e.\u0e28' in date or u'\u0e01\u0e23\u0e01\u0e0e\u0e32\u0e04\u0e21 \u0e1e.\u0e28' in date or u'\u0e21\u0e34\u0e16\u0e38\u0e19\u0e32\u0e22\u0e19 \u0e1e.\u0e28' in date or u'\u0e1e\u0e24\u0e29\u0e20\u0e32\u0e04\u0e21 \u0e1e.\u0e28' in date or u'\u0e40\u0e21\u0e29\u0e32\u0e22\u0e19 \u0e1e.\u0e28' in date:
            

        
            _date = date.replace(u'\u0e21\u0e35\u0e19\u0e32\u0e04\u0e21 \u0e1e.\u0e28','March').replace(u'\u0e19.','').replace(u'\u0e01\u0e38\u0e21\u0e20\u0e32\u0e1e\u0e31\u0e19\u0e18\u0e4c \u0e1e.\u0e28','Feb').replace(u'\u0e21\u0e01\u0e23\u0e32\u0e04\u0e21 \u0e1e.\u0e28','Jan').replace(u'\u0e18\u0e31\u0e19\u0e27\u0e32\u0e04\u0e21 \u0e1e.\u0e28','Dec').replace(u'\u0e1e\u0e24\u0e28\u0e08\u0e34\u0e01\u0e32\u0e22\u0e19 \u0e1e.\u0e28','Nov').replace(u'\u0e15\u0e38\u0e25\u0e32\u0e04\u0e21 \u0e1e.\u0e28','Oct').replace(u'\u0e01\u0e31\u0e19\u0e22\u0e32\u0e22\u0e19 \u0e1e.\u0e28','Sep').replace(u'\u0e2a\u0e34\u0e07\u0e2b\u0e32\u0e04\u0e21 \u0e1e.\u0e28','AUG').replace(u'\u0e01\u0e23\u0e01\u0e0e\u0e32\u0e04\u0e21 \u0e1e.\u0e28','JULY').replace(u'\u0e21\u0e34\u0e16\u0e38\u0e19\u0e32\u0e22\u0e19 \u0e1e.\u0e28','June').replace(u'\u0e1e\u0e24\u0e29\u0e20\u0e32\u0e04\u0e21 \u0e1e.\u0e28','May').replace(u'\u0e40\u0e21\u0e29\u0e32\u0e22\u0e19 \u0e1e.\u0e28','April')

        dt = ''.join(re.findall('\d+ [a-zA-Z].+.', _date))
        dt = dt.replace('.2560',',').replace('.2559',',').replace('.2556','')
        dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=7))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(main_txt))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','thailand_country_manual'])
        yield item.process()
