from juicer.utils import*
from dateutil import parser

class AM730HK(JuicerSpider):
    name = 'am730hk2'
    start_urls = ['http://www.am730.com.hk/fresh/article', 'http://www.am730.com.hk/section_index-1','http://www.am730.com.hk/section_index-2', 'http://www.am730.com.hk/column_list-2', 'http://www.am730.com.hk/section_index-3', 'http://www.am730.com.hk/column_list-3', 'http://www.am730.com.hk/column_list-8', 'http://www.am730.com.hk/section_index-8', 'http://www.am730.com.hk/column_list-6', 'http://www.am730.com.hk/section_index-6','http://www.am730.com.hk/column_list-9','http://www.am730.com.hk/section_index-9','http://www.am730.com.hk/column_list-13','http://www.am730.com.hk/section_index-13','http://www.am730.com.hk/column_list-12','http://www.am730.com.hk/section_index-12','http://www.am730.com.hk/section_index-10','http://www.am730.com.hk/column_list-10','http://www.am730.com.hk/column_list-30','http://www.am730.com.hk/section_index-30','http://www.am730.com.hk/section_index-11','http://www.am730.com.hk/column_list-11','http://www.am730.com.hk/section_index-37','http://www.am730.com.hk/column_list-37','http://www.am730.com.hk/column_list-7','http://www.am730.com.hk/section_index-7','http://www.am730.com.hk/column_list-32','http://www.am730.com.hk/section_index-32','http://www.am730.com.hk/column_list-33','http://www.am730.com.hk/section_index-33','http://www.am730.com.hk/column_list-34','http://www.am730.com.hk/section_index-34','http://www.am730.com.hk/section_index-38','http://www.am730.com.hk/column_list-38','http://www.am730.com.hk/column_list-5','http://www.am730.com.hk/section_index-5','http://www.am730.com.hk/column_list-4','http://www.am730.com.hk/section_index-4','http://www.am730.com.hk/section_index-14','http://www.am730.com.hk/column_list-14','http://www.am730.com.hk/shopping/column/', 'http://www.am730.com.hk/shopping/article']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@id="news_index_box"]')
        links = hdoc.select('//div[@id="column_index_name"]/a/@href').extract()

        for link in links[:2]:
            if 'http' not in link: link = 'http://www.am730.com.hk/' + link
            yield Request(link,self.parse,response)
        for node in nodes[:2]:
            date = textify(node.select('.//div[@id="news_index_date"]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            sub_links = textify(node.select('./div[@id="news_index_title"]/a/@href'))
            if 'http' not in sub_links: sub_links = 'http://www.am730.com.hk/' + sub_links
            yield Request(sub_links,self.parse_details,response)


        nxt_pg = textify(hdoc.select('//ul[@id="pagination-flickr"]/li[last()]/a/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg: nxt_pg = 'http://www.am730.com.hk/' + nxt_pg
            yield Request(nxt_pg,self.parse,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="printTopic"]/text()'))
        text =  textify(hdoc.select('//div[@id="mymain"]//text()')) or textify(hdoc.select('//div[@class="wordsnap"]//text()')) or textify(hdoc.select('//div[@id="article_content"]//p/text()')) or textify(hdoc.select('//div[@id="article_content"]//div//text()'))
        date = textify(hdoc.select('//div[@class="dateforarticle"]/text()')) or textify(hdoc.select('//div[@id="article_date"]//text()'))
        if u'\u5206\u524d' in date or u'\u5c0f\u6642' in date:
            _date = date.replace(u'\u5206\u524d','minutes ago').replace(u'\u5c0f\u6642','hour')
            _date = _date.strip('-')
            dt_added = get_timestamp(parse_date(xcode(_date)))
        else:
            _date = date.replace(u'\u5e74','-').replace(u'\u6708','-').replace(u'\u65e5','-')
            _date = _date.strip('-')
            try:
                dt_added = get_timestamp(parse_date(xcode(_date)) - datetime.timedelta(hours=8))
            except ValueError:
                import pdb;pdb.set_trace()
'''

        item = Item(response)
        item.set('url', response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        #yield item.process()'''
