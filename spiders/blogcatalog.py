from juicer.utils import *

COUNTRIES = {"jakarta"    : "indonesia",
            "bandung"     : "indonesia",
            "delhi"       : "india",
            "bangalore"   : "india",
            "chennai"     : "india",
            "hyderabad"   : "india",
            "kuala-lumpur": "malaysia",
            "singapore"   : "singapore",
            "yogyakarta"  : "indonesia",
            "bangkok"     : "thailand",
            "beijng"      : "china",
            "shanghai"    : "china",
            "shenzhen"    : "china"
            }

class BlogCatalog(JuicerSpider):
    name = 'blogcatalog'
    start_urls = ['http://www.blogcatalog.com/bloggers/city/jakarta/43',
                    'http://www.blogcatalog.com/bloggers/city/bandung',
                    'http://www.blogcatalog.com/bloggers/city/delhi',
                    'http://www.blogcatalog.com/bloggers/city/chennai',
                    'http://www.blogcatalog.com/bloggers/city/bangalore',
                    'http://www.blogcatalog.com/bloggers/city/hyderabad',
                    'http://www.blogcatalog.com/bloggers/city/kuala-lumpur',
                    'http://www.blogcatalog.com/bloggers/city/singapore',
                    'http://www.blogcatalog.com/bloggers/city/yogyakarta',
                    'http://www.blogcatalog.com/bloggers/city/bangkok',
                    'http://www.blogcatalog.com/bloggers/city/beijng',
                    'http://www.blogcatalog.com/bloggers/city/shanghai',
                    'http://www.blogcatalog.com/bloggers/city/shenzhen'
                ][:1]

    def parse(self, response):
        hdoc = HTML(response)

        #country = response.meta.get("country")
        country = "indonesia"
        if not country:
            city = response.url.split("/")[-1]
            country = COUNTRIES.get(city)

        print "country>>>>", country, response.url
        terminal_urls = hdoc.select_urls(['//div[@class="details"]//h3//a/@href'], response)
        print "terminal_urls>>>>", len(terminal_urls)
        for terminal_url in terminal_urls:
            get_page("blogcatalog_terminal", terminal_url, data=country)

        next_url = hdoc.select_urls(['//div[@class="pagination"]//a[contains(text(), "NEXT")]/@href'], response)
        print "next_url>>>", next_url, "\n"
        for url in next_url:
            yield Request(url, self.parse, response, meta = {"country" : country})

    def parse_terminal(self, response):
        hdoc = HTML(response)

        country = response.meta.get("country")
        blogs = hdoc.select_urls(['//div[@class="blog_narrow"]/p/a[@target="_blank"]/@href'], response)
        file_name = country + "_blogcatalog_sources"
        file_name = "/home/headrun/venu/rss/" + file_name
        out = file(file_name, "ab+")
        for blog_url in blogs:
            out.write("%s\n" %(blog_url))
        out.close()
