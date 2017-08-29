from juicer.utils import *
from dateutil import parser


class News18In(JuicerSpider):
    name = 'news18'
    start_urls = ['http://www.news18.com/india/','http://www.news18.com/politics/','http://www.news18.com/tech/','http://www.news18.com/movies/','http://www.news18.com/buzz/','http://www.news18.com/world/','http://www.news18.com/lifestyle/','http://www.news18.com/business/','http://www.news18.com/sports/','http://www.news18.com/auto/','http://www.news18.com/news/','http://www.news18.com/cricketnext/latestnews/']

    def parse(self,response):
        hdoc = HTML(response)
        news_links = hdoc.select('//div[@class="blog-list-blog"]/a/@href').extract() or hdoc.select('//div[@class="story_match_listing"]//li//h2/a/@href').extract()
        for link in news_links:
            if 'videos' in link or '/photogallery/' in link:
                continue
            yield Request(link,self.parse_details,response)
        if not news_links:
            is_nxt = True
            nodes = hdoc.select('//li//h3')
            for node in nodes:
                date = textify(node.select('.//span//text()'))
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node.select('.//a/@href'))
                if '/photogallery/' in link or 'videos' in link:
                    continue
                yield Request(link,self.parse_details,response)
            nxt_pg = textify(hdoc.select('//div[@class="pagination vsp10 n-mbl"]//a[@class="act"]/following-sibling::a[1]/@href'))
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse,response)

        nxt_pg = textify(hdoc.select('//div[@class="pagination"]//li[@class="next"]/a/@href')) or textify(hdoc.select('//a[@class="next fleft"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.news18.com' + nxt_pg
        yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1/text()'))
        text=textify(hdoc.select('//div[@id="article_body"]//text()')) or textify(hdoc.select('//div[@class="event-content fright"]//div[contains(@class, "lbcontent")]//text()')) or textify(hdoc.select('//article[@class="paragraph"]//text()')) or textify(hdoc.select('//div[@class="pcontener"]//p//text()'))
        junk1=textify(hdoc.select('//div[@class="tag"]//text()')) 
        junk2 = textify(hdoc.select('//div[contains(@class, "tag")]//text()'))
        junk=textify(hdoc.select('//div[@class="tag"]/preceding-sibling::style/text()'))
        junk3 = textify(hdoc.select('//div[@class="bynow nbdr"]//text()'))
        text = text.replace(junk3,'')
        author = textify(hdoc.select('//div[@class="author fleft"]/p/a[1]/text()'))
        author_url = textify(hdoc.select('//div[@class="author fleft"]/p/a[1]/@href'))
        if 'http' not in author_url: author_url = 'http://www.news18.com' + author_url
        text = text.replace(junk,'').replace(junk1,'').replace(junk2,'')
        date = textify(hdoc.select('//div[@class="bynow nbdr"]//text()')) or textify(hdoc.select('//span[@class="update_date"]//text()'))  or textify(hdoc.select('//div[@class="fleft bctextbox"]//text()'))
        if not date:
            dt = textify(hdoc.select('//div[@class="lvt-rightbox fright"]//date//text()'))
            if 'News18.com' in dt:
                dt = dt.replace('News18.com','')
            if not dt:
                dt= textify(hdoc.select('//div[@class="author fleft"]//span/strong/following-sibling::text()'))
                dt=dt.partition('|')[0]
            date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=5,minutes=30))
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(date_added))
            item.set('author', {'name':xcode(author)})
            item.set('author_url',xcode(author_url))
            item.set('xtags',['news_sourcetype_manual','india_country_manual'])
            yield item.process()


        date = ''.join( re.findall(':(.*)',date)) 
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added'xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()
