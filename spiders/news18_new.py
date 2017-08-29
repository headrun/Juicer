# -*- coding: utf-8 -*-
# encoding=utf8
from juicer.utils import*
from dateutil import parser

class News18(JuicerSpider):
    name = 'news18_new'
    start_urls = ['http://www.news18.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[contains(@class, "fleft")]/li/a/@href').extract()
        for category in categories:
            if 'http' not in category: category = 'http://www.news18.com' + category
            import pdb;pdb.set_trace()

            yield Request(category,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        import pdb;pdb.set_trace()
        #news_links = hdoc.select('//div[@class="blog-list-blog"]/a/@href').extract() or hdoc.select('//div[@class="story_match_listing"]//li//h2/a/@href').extract() or hdoc.select('//ul[@class="use-listing outer clearfix"]/li/a/@href').extract() or hdoc.select('//div[@class="banner-block"]//a/@href').extract() or hdoc.select('//div[@class="mt_tags"]//a/@href')
            #link = 'http://www.news18.com/news/tech/leeco-announces-its-big-american-dream-with-le-pro-3-and-umax85-tv-1303303.html'
        nodes = hdoc.select('//div[@class="blog-list-blog"] | //div[@class="story_match_listing"] | //ul[@class="use-listing outer clearfix"] | //div[@class="banner-block"] | //div[@class="mt_tags"]')
        for node in nodes:
            date = textify(hdoc.select('./span/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('./a/@href')) or textify(node.select('.//li//h2/a/@href')) or textify(node.select('./li/a/@href')) or textify(node.select('.//a/@href'))
            link = 'http://www.news18.com/news/tech/leeco-announces-its-big-american-dream-with-le-pro-3-and-umax85-tv-1303303.html'
            yield Request(link,self.parse_details,response)

        #nxt_pg = textify(hdoc.select('//div[@class="pagination"]//li[@class="next"]/a/@href')) or textify(hdoc.select('//a[@class="next fleft"]/@href'))
        #if 'http' not in nxt_pg: nxt_pg = 'http://www.news18.com' + nxt_pg
        #if nxt_pg and is_next:
            #yield Request(nxt_pg,self.parse_links,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1/text()'))
        date = textify(hdoc.select('//div[@class="author fleft"]/span/text()').extract()).split('IST')[0] or textify(hdoc.select('//div[@class="byline"]/text()')) or textify(hdoc.select('//div[@class="lvt-rightbox fright"]/date/text()').extract()).split('Published')[1]
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//div[@class="author fleft"]/p/a[not(contains(@class,"fttxt"))]/text()')) or textify(hdoc.select('//div[@class="byline"]/span/a/text()'))
        author_url = textify(hdoc.select('//div[@class="author fleft"]/p/a[not(contains(@class,"fttxt"))]/@href')) or textify(hdoc.select('//div[@class="byline"]/span/a/@href'))
        if 'http' not in author_url: author_url = 'http://www.news18.com' + author_url
        text = ''.join(re.findall('"articleBody":"(.*)"articleSection', response.body.replace('\n', '').replace('\r', ''))) or hdoc.select('//div[@class="pcontener"]/p/text()').extract() or hdoc.select('//div[@class="lbcontent"]/p//text()').extract()
        #text = text.replace('\xe2\x80\x94',' ')
        import pdb;pdb.set_trace()
        extra_text = ''.join(hdoc.select('//h5/text()').extract())
        text_final = extra_text.decode('utf-8') + ' ' + text.decode('utf-8')
        if title == '' or text == '' or date == '':
            import pdb;pdb.set_trace()
