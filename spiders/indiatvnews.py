from juicer.utils import*
from dateutil import parser

class IndiaTvNews(JuicerSpider):
    name = "indiatvnews"
    start_urls = ['http://www.indiatvnews.com/india/national', 'http://www.indiatvnews.com/world', 'http://www.indiatvnews.com/entertainment/tv', 'http://www.indiatvnews.com/entertainment/hollywood', 'http://www.indiatvnews.com/entertainment/bollywood', 'http://www.indiatvnews.com/entertainment/tv', 'http://www.indiatvnews.com/entertainment/masala', 'http://www.indiatvnews.com/entertainment/movie-review', 'http://www.indiatvnews.com/entertainment/regional','http://www.indiatvnews.com/sports/cricket', 'http://www.indiatvnews.com/sports/soccer', 'http://www.indiatvnews.com/sports/tennis', 'http://www.indiatvnews.com/sports/hockey', 'http://www.indiatvnews.com/sports/other', 'http://www.indiatvnews.com/t20-world-cup', 'http://www.indiatvnews.com/ipl', 'http://www.indiatvnews.com/india/national', 'http://www.indiatvnews.com/politics', 'http://www.indiatvnews.com/world', 'http://www.indiatvnews.com/buzz/mouthful', 'http://www.indiatvnews.com/buzz/who-cares', 'http://www.indiatvnews.com/buzz/life', 'http://www.indiatvnews.com/buzz/tech-auto', 'http://www.indiatvnews.com/buzz/blah', 'http://www.indiatvnews.com/business/real-estate', 'http://www.indiatvnews.com/business/markets', 'http://www.indiatvnews.com/business/tech', 'http://www.indiatvnews.com/business/auto', 'http://www.indiatvnews.com/business/economy', 'http://www.indiatvnews.com/lifestyle/beauty', 'http://www.indiatvnews.com/lifestyle/travel', 'http://www.indiatvnews.com/lifestyle/health', 'http://www.indiatvnews.com/lifestyle/fashion', 'http://www.indiatvnews.com/lifestyle/food', 'http://www.indiatvnews.com/lifestyle/dating', 'http://www.indiatvnews.com/lifestyle/celebs']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="cattdb"] | //h3[@class="stitle"] | //h2[@class="stitle"] | //h1[@class="hb"] | //h2[@class="hb"] | //h4[@class="stitle"] | //div[@class="sttb"] | //h4[@class="hs"]')

        for node in nodes:
            date = textify(node.select('.//span[@class="stsou"]/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue

            link = textify(node.select('./h4/a/@href')) or textify(node.select('./a/@href')) or textify(node.select('./h5/a/@href')) or textify(node.select('.//h3/a/@href'))
            yield Request(link,self.parse_details,response)

        next_pg = textify(hdoc.select('//li[@class="nextpb "]/a[@rel="next"]/@href'))
        if next_pg and is_next:
            yield Request(next_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="headline"]/text()'))
        text = textify(hdoc.select('//div[@id="mad-con-new"]/p//text() | //div[@id="mad-con-new"]//text()'))
        dt_added = textify(hdoc.select('//div[@class="deskt"]//text()'))
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))

        item =Item(response)
        item.set('url', response.url)
        item.set("title",title)
        item.set("text",text)
        item.set("dt_added",dt_added)
