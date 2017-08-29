from juicer.utils import *

category_list = ["tag/artists","tag/business","tag/design","tag/education","tag/fashion","tag/food","tag/groups","tag/personal","/tag/photography","tag/startups"]
class PosterousProfileBrowseSpider(JuicerSpider):
    name = 'posterousprofile_browse'
    start_urls = ['http://www.examples.posterous.com/%s' % category for category in category_list]

    def parse(self, response):
        got_page(self.name, response)

        hdoc = HTML(response)

        for url in hdoc.select_urls(['//header/h2/a/@href'], response):
            get_page(self.name, url)
        for url in hdoc.select_urls(['//div[@class="body"]//p//a[contains(text(),"Visit the site!")]/@href'], response):
            url = textify(url).split('.')[0].split('/')[-1]
            url = "http://posterous.com/people/subscribers/%s" % url
            get_page(self.name, url)
        for url in hdoc.select_urls(['//td[@class="name"]//a/@href'],response):
            url = url.replace("people","users")
            get_page('posterousprofile_terminal', url)
            
