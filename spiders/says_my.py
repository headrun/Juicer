from juicer.utils import*
from dateutil import parser
class Says_MY(JuicerSpider):
    name = 'says_my'
    start_urls = ['http://says.com/my']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav navbar-nav"]/li/a/@href').extract()
        for cat in categories:
            if 'http://klips.says.com/' in cat  or 'https://www.youtube.com/user/SAYSLive' in cat or 'http://coupon.says.com/' in cat:
                continue
            if 'http' not in cat:   cat = 'http://says.com' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="story-info"]')
        for node in nodes:
            link = textify(node.select('.//h4/a/@href'))
            if 'http' not in link:   link = 'http://says.com' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[@class="btn-loadmore"]/@href'))
        if 'http' not in nxt_pg:   nxt_pg = 'http://says.com' + nxt_pg
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[contains(@class ,"-title")]'))
        text = textify(hdoc.select('//div[@class="story-middle"]//p//text()| //div[@class="segment-head"]/h2/text()')) or textify(hdoc.select('//div[contains(@class, "col-md-10 col-md-offset-1")]//p//text()'))
        add_txt = textify(hdoc.select('//div[@class="story-desc"]//text()'))
        txt = add_txt + '' + text 
        jun_txt = textify(hdoc.select('//div[@class="fitvidWrapper"]//p/text()'))
        jun_txt1 = textify(hdoc.select('//div[@class="segment-head"]//em/text()'))
        jun_txt2 = textify(hdoc.select('//div[@class="related-content"]//p/text()'))
        jun_txt3 = textify(hdoc.select('//blockquote[@class="twitter-tweet"]//p//text()'))
        txt = txt.replace(jun_txt2, '')
        txt = txt.replace(jun_txt3, '')
        txt = txt.replace(jun_txt, '').replace('says.com', '').replace(jun_txt1, '')
        date = textify(hdoc.select('//div[@class="story-meta"]/p/text()')) or textify(hdoc.select('//p[@class="small"]/text()'))
        date = date.replace('Published by', '')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[@class="story-meta"]//a/text()')) or textify(hdoc.select('//p[@class="brand-name"]/a/text()')) 
        author_url = textify(hdoc.select('//div[@class="story-meta"]//a/@href')) or textify(hdoc.select('//p[@class="brand-name"]/a/@href')) 
        if 'http' not in author_url: author_url = 'http://says.com' + author_url
       

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(txt))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','malaysia_country_manual'])
        yield item.process()

