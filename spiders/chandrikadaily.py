from juicer.utils import *
from dateutil import parser

class Chandrikadaily(JuicerSpider):
    name = 'chandrikadaily_in'
    start_urls = ['http://www.chandrikadaily.com/kerala.aspx','http://www.chandrikadaily.com/international.aspx','http://www.chandrikadaily.com/india.aspx','http://www.chandrikadaily.com/district.aspx?id=Thiruvananthapuram','http://www.chandrikadaily.com/district.aspx?id=Kollam','http://www.chandrikadaily.com/district.aspx?id=Pathanamthitta','http://www.chandrikadaily.com/district.aspx?id=Alappuzha','http://www.chandrikadaily.com/district.aspx?id=Kottayam','http://www.chandrikadaily.com/district.aspx?id=Idukki','http://www.chandrikadaily.com/district.aspx?id=Eranakulam','http://www.chandrikadaily.com/district.aspx?id=Thrissur','http://www.chandrikadaily.com/district.aspx?id=Palakkad','http://www.chandrikadaily.com/district.aspx?id=Malappuram','http://www.chandrikadaily.com/district.aspx?id=Kozhikode','http://www.chandrikadaily.com/district.aspx?id=Wayanad','http://www.chandrikadaily.com/district.aspx?id=Kannur','http://www.chandrikadaily.com/district.aspx?id=Kasargod','http://www.chandrikadaily.com/athletics.aspx','http://www.chandrikadaily.com/football.aspx','http://www.chandrikadaily.com/cricket.aspx','http://www.chandrikadaily.com/tennis.aspx','http://www.chandrikadaily.com/othersports.aspx','http://www.chandrikadaily.com/movies.aspx','http://www.chandrikadaily.com/music.aspx','http://www.chandrikadaily.com/health.aspx','http://www.chandrikadaily.com/travel.aspx','http://www.chandrikadaily.com/religion.aspx','http://www.chandrikadaily.com/agriculture.aspx','http://www.chandrikadaily.com/dodifferent.aspx','http://www.chandrikadaily.com/obituary.aspx','http://www.chandrikadaily.com/itandinternet.aspx','http://www.chandrikadaily.com/mobiles.aspx','http://www.chandrikadaily.com/auto.aspx']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//a[@class="style3"]/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://www.chandrikadaily.com/' + link
            yield Request(link,self.parse_details,response)

        more_news = hdoc.select('//a[contains(text(),"more")]/@href').extract()
        if more_news and 'http' not in more_news: more_news = 'http://www.chandrikadaily.com/' + more_news[0]
        yield Request(more_news,self.parse,response)

        nxt = textify(hdoc.select('//a[@id="LinkNext"]/@href'))
        nxt_pg = textify(re.findall(r'morenews.*"',nxt)).strip('"')
        if nxt_pg and 'http' not in nxt_pg: nxt_pg = 'http://www.chandrikadaily.com/' + nxt_pg
        yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="contents_left_main"]//a[@class="changeBlue"]/text()'))
        auth_dt = textify(hdoc.select('//div[@class="contents_left_main"]/div[@class="contents_left_sub_head"]/text/text()'))
        date = textify(re.findall('\d+/\d+.*',auth_dt))
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5,minutes=30))
        author = textify(re.findall('.*Posted',auth_dt)).strip('-Posted')
        text = textify(hdoc.select('//div[@class="contents_left_sub_txt"]/text//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('text',xcode(text))
        yield item.process()
