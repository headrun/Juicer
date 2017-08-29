from juicer.utils import*
from dateutil import parser

class Diabetes_forum(JuicerSpider):
    name = 'forum_diabtes'
    start_urls = ['http://community.diabetes.org/discuss']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list=[302,301]
    #meta = {'dont_redirect': True,'handle_httpstatus_list': [302]}


    def parse(self,response):
        hdoc =  HTML(response)
        categories = hdoc.select('//span[@class="forumTitleHeader"]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://community.diabetes.org' + cat
            yield Request(cat,self.parse_threads,response,meta={'dont_redirect':True})
            

    def parse_threads(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()

