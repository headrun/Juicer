from juicer.utils import *
from dateutil import parser

class Dailythanthi(JuicerSpider):
    name = 'dailythanthi'
    start_urls = ['http://www.dailythanthi.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="sitemap"]//ul/li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="ListingNewsWithMEDImage"]')
        for node in nodes:
            dt = textify(node.select('.//time//text()'))
            date = dt.replace(',','/')
            if u'\u0bae\u0bc7' in date or u'\u0b8f\u0baa\u0bcd\u0bb0\u0bb2\u0bcd' in date or u'\u0bae\u0bbe\u0bb0\u0bcd\u0b9a\u0bcd' in date or u'\u0baa\u0bbf\u0baa\u0bcd\u0bb0\u0bb5\u0bb0\u0bbf' in date or u'\u0b9c\u0ba9\u0bb5\u0bb0\u0bbf' in date or u'\u0b9f\u0bbf\u0b9a\u0bae\u0bcd\u0baa\u0bb0\u0bcd' in date or u'\u0ba8\u0bb5\u0bae\u0bcd\u0baa\u0bb0\u0bcd' in date or u'\u0b9a\u0bc6\u0baa\u0bcd\u0b9f\u0bae\u0bcd\u0baa\u0bb0\u0bcd' in date or u'\u0b85\u0b95\u0bcd\u0b9f\u0bc7\u0bbe\u0baa\u0bb0\u0bcd' in date or u'\u0b86\u0b95\u0bb8\u0bcd\u0b9f\u0bcd' in date or u'\u0b9c\u0bc2\u0bb2\u0bc8' in date or u'\u0b9c\u0bc2\u0ba9\u0bcd' in date:
                date = date.replace(u'\u0bae\u0bc7','05/').replace(u'\u0b8f\u0baa\u0bcd\u0bb0\u0bb2\u0bcd','04/').replace(u'\u0bae\u0bbe\u0bb0\u0bcd\u0b9a\u0bcd','03/').replace(u'\u0baa\u0bbf\u0baa\u0bcd\u0bb0\u0bb5\u0bb0\u0bbf','02/').replace(u'\u0b9c\u0ba9\u0bb5\u0bb0\u0bbf','01/').replace(u'\u0b9f\u0bbf\u0b9a\u0bae\u0bcd\u0baa\u0bb0\u0bcd','12/').replace(u'\u0ba8\u0bb5\u0bae\u0bcd\u0baa\u0bb0\u0bcd','11/').replace(u'\u0b9a\u0bc6\u0baa\u0bcd\u0b9f\u0bae\u0bcd\u0baa\u0bb0\u0bcd','09/')
                date = date.replace(u'\u0b85\u0b95\u0bcd\u0b9f\u0bc7\u0bbe\u0baa\u0bb0\u0bcd','10/').replace(u'\u0b86\u0b95\u0bb8\u0bcd\u0b9f\u0bcd','08/').replace(u'\u0b9c\u0bc2\u0bb2\u0bc8','07/').replace(u'\u0b9c\u0bc2\u0ba9\u0bcd','06/')
                date = ''.join(re.findall(".*/ .*?",date))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a[@class="ImgCover"]/@href')).encode('utf-8')
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@calss="col-md-12 "]/a[@class="btn btn-lg btn-listing-more"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="row col-md-12 Article_Headline "]/p/following-sibling::text()')) or textify(hdoc.select('//div[@class="row col-md-12 Article_Headline "]//text()'))
        txt = textify(hdoc.select('//div[@id="ArticleDetailContent"]//div//text()'))  or textify(hdoc.select('//div[@id="ArticleDetailContent"]//text()'))
        add_txt = textify(hdoc.select('//div[@id="ArticleAbstract"]//text()'))
        text = add_txt + ' ' + txt
        date = textify(hdoc.select('//div[@class="timestamp"]/time//text()'))
        if u'\u0bae\u0bc7' in date or u'\u0b8f\u0baa\u0bcd\u0bb0\u0bb2\u0bcd' in date or u'\u0bae\u0bbe\u0bb0\u0bcd\u0b9a\u0bcd' in date or u'\u0baa\u0bbf\u0baa\u0bcd\u0bb0\u0bb5\u0bb0\u0bbf' in date or u'\u0b9c\u0ba9\u0bb5\u0bb0\u0bbf' in date or u'\u0b9f\u0bbf\u0b9a\u0bae\u0bcd\u0baa\u0bb0\u0bcd' in date or u'\u0ba8\u0bb5\u0bae\u0bcd\u0baa\u0bb0\u0bcd' in date or u'\u0b9a\u0bc6\u0baa\u0bcd\u0b9f\u0bae\u0bcd\u0baa\u0bb0\u0bcd' in date or u'\u0b85\u0b95\u0bcd\u0b9f\u0bc7\u0bbe\u0baa\u0bb0\u0bcd' in date or u'\u0b86\u0b95\u0bb8\u0bcd\u0b9f\u0bcd' in date or u'\u0b9c\u0bc2\u0bb2\u0bc8' in date or u'\u0b9c\u0bc2\u0ba9\u0bcd' in date:
            date = date.replace(u'\u0bae\u0bc7','05/').replace(u'\u0b8f\u0baa\u0bcd\u0bb0\u0bb2\u0bcd','04/').replace(u'\u0bae\u0bbe\u0bb0\u0bcd\u0b9a\u0bcd','03/').replace(u'\u0baa\u0bbf\u0baa\u0bcd\u0bb0\u0bb5\u0bb0\u0bbf','02/').replace(u'\u0b9c\u0ba9\u0bb5\u0bb0\u0bbf','01/').replace(u'\u0b9f\u0bbf\u0b9a\u0bae\u0bcd\u0baa\u0bb0\u0bcd','12/').replace(u'\u0ba8\u0bb5\u0bae\u0bcd\u0baa\u0bb0\u0bcd','11/').replace(u'\u0b9a\u0bc6\u0baa\u0bcd\u0b9f\u0bae\u0bcd\u0baa\u0bb0\u0bcd','09/')
            date = date.replace(u'\u0b85\u0b95\u0bcd\u0b9f\u0bc7\u0bbe\u0baa\u0bb0\u0bcd','10/').replace(u'\u0b86\u0b95\u0bb8\u0bcd\u0b9f\u0bcd','08/').replace(u'\u0b9c\u0bc2\u0bb2\u0bc8','07/').replace(u'\u0b9c\u0bc2\u0ba9\u0bcd','06/')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
    
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield  item.process()

