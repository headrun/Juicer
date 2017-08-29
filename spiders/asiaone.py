from juicer.utils import*
from dateutil import parser

class Asiaone(JuicerSpider):
    name = 'asiaone'
    start_urls = ['http://www.asiaone.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@data-type, "menu_item")]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.asiaone.com' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        links = hdoc.select('//div[@class="inner"]//h2[@class="header"]/a/@href').extract() or hdoc.select('//section[@class="block block-views clearfix"]//h3/a/@href').extract()
        for link in links:
            if 'http' not in link: 
                domain = ''.join(re.findall('.*.com', response.url))
                link = domain  + link
            yield Request(link,self.parse_details,response)
    
        if not links:
            add_cate = hdoc.select('//li[contains(@data-type, "menu_item")]/a/@href').extract() or hdoc.select('//ul[@class="menu nav"]//li/a/@href').extract()
            for cate in add_cate:
                if 'http' not in cate: cate = response.url  + cate
                yield Request(cate,self.parse_addlinks,response)


        nxt_pg = textify(hdoc.select('//li[@class="pager-show-more-next first last"]/a/@href')) or textify(hdoc.select('//li[@class="pager-next last"]/a/@href'))
        if 'http' not in nxt_pg:
            domain = ''.join(re.findall('.*.com', response.url))
            nxt_pg  = domain + nxt_pg
            yield Request(nxt_pg,self.parse_links,response)

    def parse_addlinks(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="region region-content"]//h3/a/@href').extract() or hdoc.select('//div[@class="view-content"]//div[@class="header"]/a/@href').extract() or hdoc.select('//div[@class="region region-content aside"]//h3/a/@href').extract()

        for link in links:
            if 'http' not in link:
                domain = ''.join(re.findall('.*.com', response.url))
                link = domain  + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//li[@class="pager-show-more-next first last"]/a/@href')) or textify(hdoc.select('//li[@class="next last"]/a[@title="Go to next page"]/@href'))
        if 'http' not in nxt_pg:
            domain = ''.join(re.findall('.*.com', response.url))
            nxt_pg = domain + nxt_pg
            yield Request(nxt_pg,self.parse_addlinks,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="page-title container"]//text()')) or textify(hdoc.select('//h1[@class="headline"]//text()')) or textify(hdoc.select('//h1[@class="node-title"]//text()')) or textify(hdoc.select('//h2[@class="story-title"]//text()'))

        date = textify(hdoc.select('//span[@class="date"]//text()')) or textify(hdoc.select('//div[contains(@class, "date")]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="article-content"]//p//text()')) or textify(hdoc.select('//div[@class="article-content"]//following-sibling::p//text()'))
        author = textify(hdoc.select('//span[@class="author"]//text()'))  or textify(hdoc.select('//div[@class="name"]//text()')) or textify(hdoc.select('//span[@class="byline"]//text()'))
        junk_txt = textify(hdoc.select('//div[@id="dfp-ad-midarticlespecial-wrapper"]//script//text()')) 
        add_txt= textify(hdoc.select('//div[@id="dfp-ad-imu1"]//script//text()')) 
        text=text.replace(junk_txt,'').replace(add_txt,'')
        author_url = textify(hdoc.select('//div[@class="name"]/a/@href'))
        if 'http' not in author_url:
            domain = ''.join(re.findall('.*.com', response.url))
            author_url = domain + author_url    
        import pdb;pdb.set_trace()
        '''

        if author:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('author',{'name':xcode(author)})
            item.set('author_url',xcode(author_url))
            item.set('xtags', ['news_sourcetype_manual', 'singapore_country_manual'])
            yield item.process()

        else:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('xtags', ['news_sourcetype_manual', 'singapore_country_manual'])
            yield item.process()'''
