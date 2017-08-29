from juicer.utils import*
from dateutil import parser
import io
import re



class Chinapress_MY(JuicerSpider):
    name = 'chinapress'
    start_urls = ['http://www.chinapress.com.my/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = ['http://www.chinapress.com.my/category/%E6%94%BF%E6%B2%BB/', 'http://www.chinapress.com.my/category/%E7%A4%BE%E4%BC%9A/','http://www.chinapress.com.my/category/%E5%9B%BD%E9%99%85/','http://www.chinapress.com.my/category/%E4%B8%AD%E6%84%8F%E9%A3%9F/','http://www.chinapress.com.my/category/%E8%BD%A6%E5%8A%A8%E5%8A%9B/','http://www.chinapress.com.my/%E6%9F%A5%E7%9C%8B%E5%B8%82%E5%9C%BA%E8%84%89%E6%90%8F/']
        for cat in categories:
            yield Request(cat,self.parse_links,response)
        sub_cates = hdoc.select('//li[contains(@id, "menu-item-1")]/a/@href').extract()
        for cate in sub_cates:
            yield Request(cate,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="latest_post_first_cp"] | //div[@class="article-content clearfix"] | //div[@class="latest_post_maibo_first"]')
        for node in nodes:
            date = textify(node.select('.//i[@class="fa fa-bar-chart post-view-parent"]//following-sibling::text() | .//time[@class="entry-date published"]/text()'))
            ext_date =  textify(node.select('.//i[@class="fa fa-tags"]/following-sibling::text()'))
            date = date.replace(ext_date,'')
            if u'\u5c0f\u65f6\u524d' in date or u'\u5929\u524d' in date or u'\u661f\u671f\u524d' in date:
                date = date.replace(u'\u5c0f\u65f6\u524d','hours ago').replace(u'\u5929\u524d','days ago').replace(u'\u661f\u671f\u524d','week ago')
            if 'ago' in date:
                dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
            else:
                date = '-'.join(re.findall('\d+',date))
                dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//div[@class="latest_post_first_content_cp"]/a/@href | .//h1/a/@href | .//div[@class="latest_post_maibo_content"]/a/@href'))
            if 'http' not in link: 
                link = link.split('=')
                link = link[-1]
                link = 'http://www.chinapress.com.my/%E5%B8%82%E5%9C%BA%E8%84%89%E6%90%8F/?post_id=' + link
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//li[@class="next"]/a/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="entry-title"]/text()'))
        text =  textify(hdoc.select('//div[@class="entry-content clearfix"]//p//text()'))
        junk_txt = textify(hdoc.select('//a/script[@type="text/javascript"]/text()'))
        junk_txt1 = textify(hdoc.select('//p[@style="color:#FF0000;text-align:center;"]/text()'))
        text = text.replace(junk_txt,'').replace(junk_txt1,'')
        date = textify(hdoc.select('//i[@class="fa fa-clock-o"]/following-sibling::time[@class="entry-date published"]/text()')) or textify(hdoc.select('//div[@class="post-view"]//i[@class="fa fa-clock-o"]/following-sibling::text()'))
        if u'\u5c0f\u65f6\u524d' in date or u'\u5929\u524d' in date or u'\u661f\u671f\u524d' in date:
            date = date.replace(u'\u5c0f\u65f6\u524d','hours ago').replace(u'\u5929\u524d','days ago').replace(u'\u661f\u671f\u524d','week ago')
        if 'ago' in date:
            dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
        else:
            date = '-'.join(re.findall('\d+',date))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','malaysia_country_manual'])
#        yield item.process()
