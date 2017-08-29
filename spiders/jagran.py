from juicer.utils import*
from dateutil import parser

class Jagran_IN(JuicerSpider):
    name = 'jagran'
    start_urls  = ['http://www.jagran.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="footer-middle-nav"]/section//ul/li/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.jagran.com' + cat
            yield Request(cat,self.parse_links,response)

        add_cate = ['http://www.jagran.com/rajya-hindi-news.html', 'http://www.jagran.com/technology-hindi.html','http://www.jagran.com/business-hindi.html']
        for cate in add_cate:
            yield Request(cate,self.parse_sub_cat,response)

    def parse_sub_cat(self,response):
        hdoc = HTML(response)
        cate = hdoc.select('//div[@class="subnav"]//ul/li/a/@href').extract() or hdoc.select('//section[@class="ddnav"]/section[@class="ddcol5 ddnavrow2"]//ul//a[strong]/@href').extract() or hdoc.select('//div[@class="tech-breadcrum"]/div[@class="container"]//ul/li/a/@href').extract()
        for cat in cate:
            if 'http' not in cat: cat = 'http://www.jagran.com' + cat
            yield Request(cat,self.parse_sub_links,response)

    def parse_sub_links(self,response):
        hdoc = HTML(response)
        if 'aidunia.jagran.com' in response.url:
            add_links = textify(hdoc.select('//div[@class="footer_link"]//a[contains(text(), "Latest News")]/@href')) 
            if add_links:
                if 'http' not in add_links: add_links = 'http://naidunia.jagran.com' + add_links
                yield Request(add_links,self.parse_links,response)
        add_link = textify(hdoc.select('//div[@id="1473835024816"]/div[@class="newsbox"]/h2/a/@href'))
        if add_link:
            if 'http' not in add_link: add_link = 'http://www.jagran.com' + add_link
            yield Request(add_link,self.parse_links,response)
        if not add_link:
            is_nxt = True
            nodes = hdoc.select('//ul[@class="listing"]/li') or hdoc.select('//div[@class="discription"]') or hdoc.select('//div[@class="articletxtCon"]')
            for node in nodes:
                date = textify(node.select('.//span[@class="date-cat"]//text()')) or textify(node.select('./small//text()')) or textify(node.select('.//div[@class="cat"]//text()'))
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node.select('./a/@href')) or textify(node.select('.//h3/a/@href')) or textify(node.select('./h4/a[@title]/@href'))
                if 'http' not in link: link = 'http://www.jagran.com' + link
                yield Request(link,self.parse_details,response)

            extra_links = hdoc.select('//div[@class="list_con"]//div[@class="panel"]/p/a[img]/@href').extract()
            for lin in extra_links:
                if 'http' not in lin: lin = 'http://www.jagran.com' + lin
                yield Request(lin,self.parse_details,response)

            nxt_pg = textify(hdoc.select('//div[@class="listingcol"]//preceding::div[@class="pagination"]//a[contains(@title, "Next")]/@href')) or textify(hdoc.select('//div[@class="listpager"]//a[@class="next-btn"]/@href')) or textify(hdoc.select('//div[@class="mpagearticlelist"]//following::div[@class="sharebox"]//a[@class="next-btn"]/@href'))
            if 'http' not in nxt_pg: nxt_pg =  'http://www.jagran.com' + nxt_pg
            if nxt_pg  and is_nxt:
               yield Request(nxt_pg,self.parse_sub_links,response)
        
    def parse_links(self,response):
        hdoc = HTML(response)
        if 'aidunia.jagran.com' in response.url:
            is_nxt = True
            nodes = hdoc.select('//div[@class="right-listing"]')
            for node in nodes:
                date = textify(node.select('.//div[@class="time"]//text()'))
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node.select('./h3/a/@href'))
                if 'http' not in link: link = 'http://naidunia.jagran.com' + link
                yield Request(link,self.parse_details,response)
            nxt_pg = textify(hdoc.select('//div[@class="pagination"]//li//a[contains(@title, "Next")]/@href'))
            if 'http' not in nxt_pg: nxt_pg =  'http://naidunia.jagran.com' +  nxt_pg
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_links,response)

        add_nodes =  hdoc.select('//ul[@class="listing"]/li') or hdoc.select('//div[@class="articletxtCon"]')
        is_nxt = True
        for add_node in add_nodes:
            date = textify(add_node.select('.//span[@class="date-cat"]//text()')) or textify(add_node.select('.//div[@class="cat fl"]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(add_node.select('./a/@href')) or textify(add_node.select('./h2/a/@href'))
            if 'http' not in link: link = 'http://www.jagran.com' + link
            yield Request(link,self.parse_details,response)
        ext_links = hdoc.select('//div[@class="hightlight"]//li/a[@title]/@href').extract()
        for lin in ext_links:
            if 'http' not in lin: lin = 'http://www.jagran.com' + lin

        nxt_pg = textify(hdoc.select('//div[@class="listingcol"]//preceding::div[@class="pagination"]//a[contains(@title, "Next")]/@href'))or textify(hdoc.select('//div[@class="mpagearticlelist"]//following::div[@class="sharebox"]//a[@class="next-btn"]/@href'))
        if 'http' not in nxt_pg: nxt_pg =  'http://www.jagran.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)
      

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//section[@class="title"]/h1[@itemprop="headline"]//text()')) or textify(hdoc.select('//div[@class="article-details"]//h1//text()'))
        txt = textify(hdoc.select('//div[@itemprop="articleBody"]//p[not(a)]//text()')) or textify(hdoc.select('//div[@class="article-details"]//p[not(@facebook-like)]//text()'))
        sub_txt = textify(hdoc.select('//div[@itemprop="articleBody"]//div[@class="article-summery"]//text()'))
        junk_txt = textify(hdoc.select('//div[@class="facebook-like"]/p//text()'))
        txt = txt.replace(junk_txt,'')
        text =  sub_txt + ' ' +txt
        date= textify(hdoc.select('//section[@class="grayrow"]//span[@itemprop="author"]//following-sibling::span//text()')) or textify(hdoc.select('//div[@class="date fl"]//text()'))
        date=''.join(re.findall('(.*) \|',date))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//section[@class="grayrow"]//span[@itemprop="author"]//text()')) or textify(hdoc.select('//div[@class="datebox"]//span[@class="fr"]//text()'))
        if 'By' in author:
            author = author.replace('By','')
       

        item =  Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()



