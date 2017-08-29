from juicer.utils import *
from dateutil import parser
class Mb_ph(JuicerSpider):
    name = 'mb_ph'
    start_urls = ['http://mb.com.ph/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="uk-navbar-nav uk-hidden-small"]//a[contains(@class, "uk-display-block")]/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)
        cate = ['http://entertainment.mb.com.ph/category/entertainment/','http://news.mb.com.ph/category/opinions-and-editorials/','http://news.mb.com.ph/category/offbeat/']
        for category in cate:
            yield Request(category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="uk-panel"]')
        for node in nodes:
            date = textify(node.select('./ul[@class="uk-article-meta uk-subnav"]//time/text()'))
            dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h3/a/@href'))
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//ul[@class="uk-pagination"]//a[i[@class="uk-icon-angle-double-right"]]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="uk-article-title uk-margin-bottom-remove"]/text()'))
        extra_txt = hdoc.select('//div[@class="tm-main uk-width-medium-1-2"]//p')[:-1]
        text1 = textify(extra_txt.select('.//text()').extract())
        text = textify(hdoc.select('//div[@class="tm-main uk-width-medium-1-2"]//p[@style="text-align: justify;"]//p[not(contains(@class, "wp-caption-text"))]/text() | //p[@style="text-align: justify;"]//text()')) or text1 or textify(hdoc.select('//p[@class="wp-caption-text"]//text()'))

        #text = text.replace('Tags:','').strip(', ')
        date = textify(hdoc.select('//div[@class="published_date"]/time/text()'))
        if not date:
            date = textify(hdoc.select('//div[@class="updated_date"]/time/text()'))
        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=8))
        author = textify(hdoc.select('//h3[@class="uk-h5 uk-margin-small-bottom"]/a[@class="author url fn"]/text()')) or textify(hdoc.select('//p[@style="text-align: justify;"]/em//text()'))
        if not author:
            author = textify(hdoc.select('//p/strong/em/text()')) or textify(hdoc.select('//p/em/strong/text()'))
        auth_url = textify(hdoc.select('//h3[@class="uk-h5 uk-margin-small-bottom"]/a[@class="author url fn"]/@href'))
        author = author.replace('By','').replace('by','')
        
        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text', xcode(text)
        print 'dt_added', xcode(dt_added)
        print 'author', xcode(author)
        print 'author_url', xcode(auth_url)
        import pdb;pdb.set_trace()
