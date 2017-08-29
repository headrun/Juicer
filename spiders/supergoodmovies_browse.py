from juicer.utils import *

class SuperGoodMoviesBrowseSpider(JuicerSpider):
    name = 'supergoodmovies_browse'
    allow_domain = 'supergoodmovies.com'
    start_urls = 'http://www.supergoodmovies.com/tollywood/movie-reviews'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = "http://www.supergoodmovies.com/news/reviewssearchlist/?industrytypeid=1&contenttypeid=1&infotypeid=8&pagenumber=%d"
        next_urls = [url % i for i in range(1, 26)]

        for next_url in next_urls:
            get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls('//h2[@class="det_ntitle"]/a/@href', response)
        for terminal_url in terminal_urls:
            get_page('supergoodmovies_terminal', terminal_url)
