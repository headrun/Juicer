from juicer.utils import *
from dateutil import parser

class YouthCn(JuicerSpider):
    name = "youth_cn"
    start_urls = ['http://news.youth.cn/sz/?src=index','http://news.youth.cn/gn/?src=index','http://news.youth.cn/sh/?src=index','http://news.youth.cn/gj/?src=index','http://news.youth.cn/yl/?src=index','http://news.youth.cn/js/?src=index','http://news.youth.cn/jk/?src=index','http://news.youth.cn/ss/?src=index','http://news.youth.cn/kj/?src=index','http://news.youth.cn/zc/?src=index','http://news.youth.cn/jy/?src=index','http://news.youth.cn/jsxw/?src=index','http://news.youth.cn/rdzt/?src=index','http://news.youth.cn/djch/?src=index','http://fun.youth.cn/gnzx/','http://fun.youth.cn/hwzx/','http://fun.youth.cn/zy/','http://fun.youth.cn/ys/','http://fun.youth.cn/bl/','http://fun.youth.cn/mt/','http://style.youth.cn/hot/','http://style.youth.cn/plan/','http://style.youth.cn/married/','http://style.youth.cn/emotion/star/','http://style.youth.cn/emotion/horoscope/','http://style.youth.cn/emotion/sexes/','http://style.youth.cn/fashion/cosmetology/','http://style.youth.cn/fashion/body/','http://style.youth.cn/fashion/man/','http://style.youth.cn/fashion/vane/','http://finance.youth.cn/finance_stock/','http://finance.youth.cn/finance_insurance/','http://finance.youth.cn/finance_bank/','http://mil.youth.cn/zxxx/','http://sports.youth.cn/sportsnews/NBA/','http://sports.youth.cn/sportsnews/jskx/','http://sports.youth.cn/sportsnews/CBA/','http://sports.youth.cn/sportsnews/gnzq/','http://sports.youth.cn/sportsnews/football/','http://sports.youth.cn/sportsnews/mjss/','http://health.youth.cn/meirong/','http://health.youth.cn/bj/','http://health.youth.cn/cj/','http://health.youth.cn/mt/','http://health.youth.cn/ys/','http://health.youth.cn/yd/','http://health.youth.cn/nx/','http://health.youth.cn/nanxing/','http://health.youth.cn/lx/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//li/font') 
        for node in nodes:
            date =  textify(node.select('.//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link =  textify(node.select('./following-sibling::a/@href'))
            if 'http' not in link: 
                if '?src=' in response.url:
                    domain = ''.join(re.findall('(.*?)\?', response.url))
                    url = domain + link
                else:
                    domain = ''.join(re.findall('(.*/)?', response.url))        
                    url = domain + link
                yield Request(url,self.parse_details,response)
            else:
                yield Request(link,self.parse_details,response)

        if not nodes:
            ext_nodes = hdoc.select('//li[@class="item"]//a[@class="title"]/@href').extract() or hdoc.select('//li//a[@class="box_news"]/@href').extract()
            for lin in ext_nodes:
                if 'http' not in lin: 
                    domain = ''.join(re.findall('(.*/)?', response.url))     
                    ext_url = domain + lin
                yield Request(ext_url,self.parse_details,response)


        for i in range(1,50):
            if '?src' in response.url:
                domain = ''.join(re.findall('(.*?)\?', response.url))
                nxt_pg = domain + 'index_%s.htm' % i 
            else:
                domain = ''.join(re.findall('(.*/)?', response.url))
                nxt_pg = domain + 'index_%s.htm' % i

            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="l_tit"]//text()')) or textify(hdoc.select('//div[@class="page_title"]/h1//text()'))

        if not title:
            title = textify(hdoc.select('//div[@class="pic_main_tit"]/text()'))
        text = textify(hdoc.select('//div[@class="TRS_Editor"]//p//text()')) or textify(hdoc.select('//div[@id="container"]//p//text()'))

        if not text:
            text = textify(hdoc.select('//div[@id="content"]//p//text()'))

        date=textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))  or textify(hdoc.select('//span[@id="page_right"]//text()'))

        dt = ''.join(re.findall('\d{4}-\d{2}-\d{2}', date))
        dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
        auth=author.replace(u'\u8d23\u4efb\u7f16\u8f91\uff1a','')

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(auth)})
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()



