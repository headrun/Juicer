from juicer.utils import *
from dateutil import parser

class Dzwww(JuicerSpider):
    name = "dzwww_china"
    start_urls = ['http://www.dzwww.com/xinwen/guoneixinwen/','http://www.dzwww.com/xinwen/guojixinwen/','http://www.dzwww.com/xinwen/shehuixinwen/','http://www.dzwww.com/dzwpl/gdyc/','http://www.dzwww.com/dzwpl/mspl/','http://www.dzwww.com/dzwpl/gdwp/','http://www.dzwww.com/dzwpl/gdzt/','http://www.dzwww.com/dzwpl/ms/','http://www.dzwww.com/dzwpl/gdzl/','http://www.dzwww.com/dzwpl/gddb/','http://www.dzwww.com/dzwpl/cj/','http://www.dzwww.com/dzwpl/sz/','http://www.dzwww.com/dzwpl/wt/','http://www.dzwww.com/2009jczt/gnzt/','http://www.dzwww.com/2009jczt/gjzt/','http://www.dzwww.com/2009jczt/sdzt/','http://www.dzwww.com/2009jczt/shzt/','http://www.dzwww.com/2009jczt/sdbd/','http://www.dzwww.com/2009jczt/wszt/','http://www.dzwww.com/2009jczt/playzt/','http://www.dzwww.com/2009jczt/sportszt/','http://www.dzwww.com/2009jczt/dszt/','http://www.dzwww.com/2009jczt/jczthz/','http://ent.dzwww.com/gt/','http://ent.dzwww.com/om/','http://ent.dzwww.com/rh/','http://ent.dzwww.com/yy/','http://ent.dzwww.com/dy/','http://ent.dzwww.com/ds/','http://ent.dzwww.com/zy/','http://ent.dzwww.com/pl/','http://ent.dzwww.com/xp/','http://sports.dzwww.com/jszx/','http://sports.dzwww.com/news/','http://sports.dzwww.com/global/gjzq/','http://sports.dzwww.com/china/rdjj/','http://sports.dzwww.com/basketball/nba/','http://sports.dzwww.com/basketball/gnlq/','http://sports.dzwww.com/zhty/rdjj/','http://sports.dzwww.com/tthx/','http://lady.dzwww.com/yw/','http://lady.dzwww.com/zb/','http://lady.dzwww.com/ny/','http://lady.dzwww.com/sex/','http://lady.dzwww.com/mr/','http://lady.dzwww.com/hz/','http://lady.dzwww.com/mt/','http://lady.dzwww.com/jk/','http://lady.dzwww.com/yyjk/','http://lady.dzwww.com/qz/','http://finance.dzwww.com/jiaodian/jrtt/','http://finance.dzwww.com/sdcj/','http://finance.dzwww.com/jiaodian/zhuanti/','http://finance.dzwww.com/jiaodian/zxbb/','http://finance.dzwww.com/cjyl/','http://finance.dzwww.com/khql/khzx/','http://finance.dzwww.com/khql/ykbk/','http://house.dzwww.com/news/yw/','http://house.dzwww.com/news/dcrw/','http://home.dzwww.com/jjsj/','http://home.dzwww.com/jrtt/','http://house.dzwww.com/news/jingcaishenghuo/','http://house.dzwww.com/news/bbs/fitmentgroup/','http://edu.dzwww.com/dzjyxw/redian/','http://health.dzwww.com/jkxw/shgz/','http://health.dzwww.com/jkxw/jrxw/','http://health.dzwww.com/jkxw/yydt/','http://health.dzwww.com/jkxw/yg/','http://health.dzwww.com/jkxw/food/','http://health.dzwww.com/ysbj/','http://health.dzwww.com/jkxw/xwtj/','http://health.dzwww.com/yjft/gdft/','http://health.dzwww.com/jkzjt/','http://tour.dzwww.com/gdnews/','http://auto.dzwww.com/qlcyh/sj/','http://auto.dzwww.com/dg/dg/','http://auto.dzwww.com/news/xc/','http://auto.dzwww.com/cw/hq/','http://auto.dzwww.com/yc/bywx/','http://auto.dzwww.com/yc/yczx/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//li/h3')
        for node in nodes:
            date = textify(node.select('.//following-sibling::div[@class="bottom"]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a[@target="_blank"]/@href'))
            if 'http' not in link: 
                main_link = response.url + link
                yield Request(main_link,self.parse_details,response)
            if 'default_' in response.url:
                domain = ''.join(re.sub(r'default(.*)', '', response.url))
                main_link = domain + link
                yield Request(main_link,self.parse_details,response)
        if not date:
            links = hdoc.select('//h3/a/@href').extract()
            for lin in links:
                yield Request(lin,self.parse_details,response)
                


        for i in range(1,150):
            nxt_pg  = response.url + 'default_%s.htm' % i
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse,response)
        if 'default' in response.url:
            domain = ''.join(re.sub(r'default(.*)', '', response.url))
            next_page = domain + 'default_%s.htm' % i
            yield Request(next_page,self.parse,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="layout"]//h2//text()')) or textify(hdoc.select('//div[@class="blank40"]/following-sibling::h1//text()')) or textify(hdoc.select('//div[@class="top"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="TRS_Editor"]//p//text()')) or textify(hdoc.select('//div[@class="news-con"]//p//text()')) or textify(hdoc.select('//div[@class="TRS_Editor"]//text()')) or textify(hdoc.select('//div[@class="con"]//p//text()'))
        add_txt = textify(hdoc.select('//div[@class="summary"]//text()'))
        text = add_txt + ' ' + text
        dt = textify(hdoc.select('//div[@class="layout"]//div[@class="left"]//text()')) or textify(hdoc.select('//div[@class="left"]/span//text()')) or textify(hdoc.select('//div[@class="top"]//h1//following-sibling::p/text()'))
        date = ''.join(re.findall('\d{4}-\d{2}-\d{2}', dt))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author1 = textify(hdoc.select('//div[@class="text"]/p[1]//text()')) or textify(hdoc.select('//div[@class="EDIT"]//span//text()'))
        author1 = author1.replace(u'\u521d\u5ba1\u7f16\u8f91\uff1a','')
        author2 = textify(hdoc.select('//div[@class="text"]/p[last()]//text()'))
        author2 = author2.replace(u'\u8d23\u4efb\u7f16\u8f91\uff1a','')


        item = Item(response)
        item.set('url', response.url))
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(dt_added))
        item.set('author',{'name':xcode(author1)})
        item.set('author',{'name':xcode(author2)})
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()
