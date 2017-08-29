from juicer.utils import *

class Baidu(JuicerSpider):
    name = "zhidao_baidu"
    start_urls = ['http://zhidao.baidu.com/browse/']

    def parse(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        print "response.url >>>>", response.url
        category_urls = hdoc.select_urls(['//li[@class="category-item"]//a[contains(@href, "/browse/")]/@href'], response)

        category_urls = list(set(category_urls))
        out = file("/home/headrun/venu/rss/zhidao_baidu_feeds", "ab+")
        for category in category_urls:
            category_id = ''.join(re.findall(r'browse/(\d+)', category))
            if category_id:
                rss_url = 'http://zhidao.baidu.com/q?ct=18&cid=%s&lm=2&rn=25&tn=rssql&md=8' %(str(category_id))
                print "rss_url>>>>", rss_url
                out.write("%s\n" %(rss_url))

        out.close()

        for cat in category_urls:
            yield Request(cat, self.parse, response)
