from juicer.utils import *

class BokeeSpider(JuicerSpider):
    name = 'bokee_browse'
    allowed_domains = ['bokee.com']
    start_urls = ['http://mm.bokee.com/', 'http://life.bokee.com/', 'http://ent.bokee.com/', 'http://fashion.bokee.com/', 'http://love.bokee.com/', 'http://news.bokee.com/', 'http://2012.bokee.com/']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//div[contains(@class, "notice_")]//ul//li//a/@href'], response)

        for navigation_url in navigation_urls:
            print "navigation_url>>>>>>>>>>>", navigation_url
            get_page(self.name, navigation_url)

        terminal_urls = hdoc.select_urls(['//a[contains(@href, "/viewdiary.")]/@href'], response)

        for terminal_url in terminal_urls:
            print "terminal_urs>>>>>>>>", terminal_url
            get_page('bokee_terminal', terminal_url)
