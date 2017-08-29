from juicer.utils import *
import feedparser

class Business_standard(JuicerSpider):
    name = 'business_standard'

    def start_requests(self):
        requests = []
        articles_data = file('/home/headrun/venu/business_standard_data', 'r').readlines()
        for article_data in articles_data:
            article_data = article_data.replace('\n','').split('\t')
            feed_url = article_data[0].strip()
            article_url = article_data[1].strip()
            feed_text = article_data[-1].strip()
            print article_url
            try:
                r = Request(article_url, self.parse, None, meta={'feed_url' : feed_url, "feed_text" : feed_text})
                requests.extend(r)
            except: pass

        return requests

    def parse(self, response):

        feed_url = response.meta['feed_url'].encode('utf8').decode('ascii','ignore')
        feed_text = response.meta['feed_text'].encode('utf8').decode('ascii','ignore')
        article_url = response.url.encode('utf8').decode('ascii','ignore')

        #print response.url
        hdoc = HTML(response)
        article_text = textify(hdoc.select('//div[@class="colL_MktColumn2"]//text()')).encode('utf8').decode('ascii','ignore')

        out_file = file('/home/headrun/venu/business_standard_data_final', 'ab+')
        out_file.write('%s\t%s\t%s\t%s\n' %(feed_url, article_url, feed_text, article_text))
        out_file.close()

