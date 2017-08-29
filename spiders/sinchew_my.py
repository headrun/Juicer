from juicer.utils import*
from dateutil import parser

class Sinchew_MY(JuicerSpider):
    name = 'sinchew_my'
    start_urls = ['http://www.sinchew.com.my/%E6%96%B0%E8%81%9E/%E5%9B%BD%E5%86%85']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list = [403]

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        categories = hdoc.select('//div[@class="menu-subsection col-xs-6"]/a/@href').extract()
        for cat in categories:
            import pdb;pdb.set_trace()
            if 'http' not in cat: cat = 'http://www.sinchew.com.my' + cat
            yield Request(cat,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="post-excerpt-one-column-view"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="date-created"]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
            link = textify(node.select('./h2/a/@href'))
            if 'http' not in link: link = 'http://www.sinchew.com.my' + link
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//ul[@class="pager"]//li[@class="pager-next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.sinchew.com.my' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)
    
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="page-title"]/text()'))
        date = textify(hdoc.select('//div[@class="date-created"]/text()'))
        add_txt = textify(hdoc.select('//div[@class="caption-in-slide"]/text()'))
        text = textify(hdoc.select('//div[@class="content clearfix"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="images-slider-wrapper"]/following-sibling::text()'))
        main_txt = add_txt + ' ' + text
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))

"""
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(main_txt))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags', ['news_sourcetype_manual', 'malaysia_country_manual'])
        yield item.process()
        """
