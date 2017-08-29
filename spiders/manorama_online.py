from juicer.utils import *
from dateutil import parser

class ManoramaOnline(JuicerSpider):
    name = "manorama"
    start_urls = ['http://english.manoramaonline.com/news/just-in.html','http://english.manoramaonline.com/news/nation.html','http://english.manoramaonline.com/news/politics.html','http://english.manoramaonline.com/news/science-technology.html','http://english.manoramaonline.com/news/kerala.html','http://english.manoramaonline.com/news/world.html','http://english.manoramaonline.com/sports/cricket.html','http://english.manoramaonline.com/sports/cricket.html','http://english.manoramaonline.com/sports/tennis.html','http://english.manoramaonline.com/sports/motor-sports.html','http://english.manoramaonline.com/sports/other-sports.html','http://english.manoramaonline.com/business/news.html','http://english.manoramaonline.com/business/companies.html','http://english.manoramaonline.com/business/stocks-live.html','http://english.manoramaonline.com/business/autos.html','http://english.manoramaonline.com/business/markets.html','http://english.manoramaonline.com/business/markets.html','http://english.manoramaonline.com/business/markets.html','http://english.manoramaonline.com/business/markets.html','http://english.manoramaonline.com/in-depth/dakshin-dare-14.html','http://english.manoramaonline.com/in-depth/sabarimala.html','http://english.manoramaonline.com/in-depth/india-wi-series.html','http://english.manoramaonline.com/in-depth/prohibition-pangs.html','http://english.manoramaonline.com/lifestyle/fashions.html','http://english.manoramaonline.com/lifestyle/beauty.html','http://english.manoramaonline.com/lifestyle/gala.html','http://english.manoramaonline.com/lifestyle/gala.html','http://english.manoramaonline.com/lifestyle/health.html','http://english.manoramaonline.com/lifestyle/decor.html','http://english.manoramaonline.com/entertainment/entertainment-news.html','http://english.manoramaonline.com/entertainment/movie-reviews.html','http://english.manoramaonline.com/entertainment/art-and-culture.html','http://english.manoramaonline.com/entertainment/interview.html','http://english.manoramaonline.com/entertainment/music.html','http://english.manoramaonline.com/entertainment/gossip.html','http://travel.manoramaonline.com/travel.html','http://food.manoramaonline.com/food.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//section[@class="other-story-sc pglParWrap"]//article//h4//a//@href')
        for url in urls:
            yield Request(url, self.parse_details, response)

    def parse_details(self, response):
        hdoc = HTML(response)

        title = textify(hdoc.select('//header[@class="articleTop"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="article"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@class="entryDate"]//text()'))
        author = textify(hdoc.select('//div[@class="author"]//h3[@class="authorName"]/text()'))
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))
"""
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        yield item.process()


        """
