from juicer.utils import*
from dateutil import parser

class IndinaExpress(JuicerSpider):
    name = 'indianexpress'
    start_urls = ['http://indianexpress.com/section/india/', 'http://indianexpress.com/section/world/','http://indianexpress.com/section/business/','http://indianexpress.com/section/cities/','http://indianexpress.com/section/sports/','http://indianexpress.com/section/entertainment/','http://indianexpress.com/section/lifestyle/','http://indianexpress.com/section/technology/','http://indianexpress.com/section/opinion/','http://indianexpress.com/section/education/','http://indianexpress.com/section/explained/','http://indianexpress.com/section/good-news/','http://indianexpress.com/trending/','http://indianexpress.com/photo-news/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[contains(@class, "articles")]')
        for node in nodes:
            date = textify(node.select('.//div[@class="date"]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//div[@class="title"]/a/@href'))
            yield Request(link,self.parse_details,response)
            if not link:
                cate = hdoc.select('//div[@class="page-nav"]/ul/li/a/@href').extract()
                for cat in cate:
                    if 'http' not in cat: cat = 'http://indianexpress.com' +  cat
                    yield Request(cat,self.parse_sublinks,response)


        if not nodes:
            links = hdoc.select('//div[@class="leadstory"]//h6/a/@href | //div[@class="opi-story"]//h6/a/@href').extract() or hdoc.select('//div[@class="top-article"]//h3/a/@href').extract()
            for linke in links:
                yield Request(linke,self.parse_details,response)
                
        nxt_pg = textify(hdoc.select('//div[@class="pagination"]//ul/li/a[@class="next page-numbers"]/@href')) or textify(hdoc.select('//a[@class="next page-numbers"]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse,response)

    def parse_sublinks(self,response):
        hdoc = HTML(response)
        link = hdoc.select('//div[@class="articles"]//h3/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//div[@class="trend-pagination"]//a[@class="next page-numbers"]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse_sublinks,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="headline"]//text()')) or textify(hdoc.select('//div[@class="commentbx"]/following-sibling::h1//text()'))
        add_txt = textify(hdoc.select('//h2[@itemprop="description"]//text()'))
        main_txt =textify(hdoc.select('//div[@itemprop="articleBody"]//p//text() | //div[@itemprop="articleBody"]//div//text()')) or textify(hdoc.select('//div[@class="rightsec"]//p//text()'))
        junk_txt = textify(hdoc.select('//div[@class="editor"]//text()')) 
        ju_txt = textify(hdoc.select('//p[@class="appstext"]//text()'))
        ext_txt = textify(hdoc.select('//div[@class="storytags"]//text()'))
        ext_txt1 = textify(hdoc.select('//ol[@class="commentlist"]//div//text()'))
        main_txt = main_txt.replace(junk_txt,'').replace(ju_txt,'')
        main_txt = main_txt.replace(ext_txt,'').replace(ext_txt1,'')
        text = add_txt + '' + main_txt
        date = textify(hdoc.select('//meta[@itemprop="datePublished"]/@content')) or textify(hdoc.select('//div[@class="date left"]//span//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        author1= textify(hdoc.select('//div[@class="editor"]/a[@id="written_by1"]//text()'))
        author2 = textify(hdoc.select('//div[@class="editor"]/a[@id="written_by2"]//text()'))
        author1_url  = textify(hdoc.select('//div[@class="editor"]/a[@id="written_by1"]//@href'))
        author2_url = textify(hdoc.select('//div[@class="editor"]/a[@id="written_by2"]//@href'))
        if not author1:
            auth = textify(hdoc.select('//div[@class="editor"]//a//text()')) or textify(hdoc.select('//div[@class="date left"]//p/a/text()')) or textify(hdoc.select('//div[@class="editor"]/text()'))
            if '|' in auth:
                auth = ''.join(re.findall('Written by(.*)', auth.split('|')[0].replace('\t', ''))).strip()
            auth_url = textify(hdoc.select('//div[@class="editor"]//a//@href')) or textify(hdoc.select('//div[@class="date left"]//p/a/@href'))
            if 'http' not in auth_url: auth_url = 'http://indianexpress.com' + auth_url
        
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        if author1:
            item.set('author', {'name':xcode(author1)})
            item.set('author_url',xcode(author1_url))
        if author2:
            item.set('author', {'name':xcode(author2)})
            item.set('author_url',xcode(author2_url))
        if not author1:
            item.set('author', {'name':xcode(auth)})
            item.set('author_url',xcode(auth_url))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()
