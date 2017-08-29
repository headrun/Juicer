from juicer.utils import*
from dateutil import parser

class Nst_MY(JuicerSpider):
    name = 'nst_my'
    start_urls = ['http://www.nst.com.my/news/crime-courts','http://www.nst.com.my/news/exclusive','http://www.nst.com.my/news/government-public-policy','http://www.nst.com.my/news/nation','http://www.nst.com.my/news/politics','http://www.nst.com.my/lifestyle/sunday-vibes','http://www.nst.com.my/lifestyle/bots','http://www.nst.com.my/lifestyle/heal','http://www.nst.com.my/lifestyle/flair','http://www.nst.com.my/lifestyle/jom','http://www.nst.com.my/lifestyle/pulse','http://www.nst.com.my/lifestyle/groove','http://www.nst.com.my/sports/football','http://www.nst.com.my/sports/badminton','http://www.nst.com.my/sports/mma','http://www.nst.com.my/sports/motor-sports','http://www.nst.com.my/sports/tennis','http://www.nst.com.my/sports/golf','http://www.nst.com.my/sports/others','http://www.nst.com.my/opinion/columnist','http://www.nst.com.my/opinion/letters','http://www.nst.com.my/opinion/leaders','http://www.nst.com.my/photos','http://www.nst.com.my/infographics','http://www.nst.com.my/business','http://www.nst.com.my/property','http://www.nst.com.my/education','http://www.nst.com.my/actionline','http://www.nst.com.my/cbt','http://www.nst.com.my/world']

    def parse(self,response):
        hdoc = HTML(response)
        if '.nst.com.my/opinion/columnist' in response.url:
            links = hdoc.select('//div[@class="views-row-inner"]//div[contains(@class, "views-field-title")]//a/@href').extract()
            for linke in links:
                if 'http' not in linke: linke= 'http://www.nst.com.my' + linke
                yield Request(linke,self.parse_details,response)

        is_nxt = True
        nodes = hdoc.select('//div[@class="views-row-inner"]')
        for node in nodes:
            date = textify(node.select('.//div[contains(@class, "views-field-created")]//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added <  get_current_timestamp()-86400*30:
               is_nxt = False
               continue
            link = textify(node.select('.//div[contains(@class, "views-field-title")]//a/@href'))
            if 'http' not in link:  link = 'http://www.nst.com.my' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//li[@class="pager-next"]//a[@title="Go to next page"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.nst.com.my' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="page-header"]//text()'))
        text = textify(hdoc.select('//div[@class="field-items"]//p//text()'))
        date = textify(hdoc.select('//span[@class="post-date"]//text()'))
        dt_added = get_timestamp (parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//span[@class="author"]/a//text()'))
        auth_url = textify(hdoc.select('//span[@class="author"]/a//@href'))
        if 'http' not in auth_url: auth_url = 'http://www.nst.com.my' +  auth_url

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(auth_url))
        item.set('xtags',['news_sourcetype_manual','malaysia_country_manual'])
        yield item.process()
            

