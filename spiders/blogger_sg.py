from juicer.utils import *

class Blogger_Singapore(JuicerSpider):
    name = 'blogger_sg'

    def start_requests(self):
        requests = []
        digits = []

        lines = file('/home/headrun/venu/blogger_urls','r').readlines()
        for line in lines:
            digit = re.findall(r'SG&start=(\d+)&ct', line)[0]
            digits.append(int(digit))

        i, j = max(digits), max(digits)+200
        for counter in xrange(i, j, 10):
            url = "http://www.blogger.com/profile-find.g?t=l&loc0=SG&start=%s&ct=KlgKOPf3djoZ_hcaipielp7Fz8_Pz8_PzMrHmpydx52dz8XGxcbeyMnIysnLx8fMyMvIycrKzMnKx__-EPoBIXIfBLoAieZhMRHsPqiuUoYBOXXl6AHmxYkI" % str(counter)
            out_file = file('/home/headrun/venu/blogger_urls', 'ab+')
            out_file.write('%s\n'%(url))
            out_file.close()
            requests.extend(Request(url, self.parse, None))

        return requests

    def parse(self, response):
        hdoc = HTML(response)

        digit = ''.join(re.findall(r'SG&start=(\d+)&ct=', response.url))
        if digit:print response.url

        blogger_urls = hdoc.select_urls(['//h2/a/@href'], response)
        for blogger_url in blogger_urls:
            yield Request(blogger_url, self.parse_sub, response)

    def parse_sub(self, response):
        hdoc = HTML(response)

        blog_urls = hdoc.select_urls(['//ul/li[@class="sidebar-item"]//a/@href'], response)
        cat = 'BLOGS'
        country = 'SINGAPORE'
        for blog_url in blog_urls:
            out_file = file('/home/headrun/venu/blogger_sg_feeds','ab+')
            if blog_url.endswith('/'):
                url = blog_url + 'feeds/posts/default?alt=rss'
            else:
                url = blog_url+'/feeds/posts/default?alt=rss'
            out_file.write('%s\t%s\t%s\n' %(url,cat,country))
            out_file.close()
