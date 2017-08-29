from juicer.utils import *

class PosterousSpaceTerminalSpider(JuicerSpider):
    name = 'posterousspace_terminal'
    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        req_url = get_request_url(response)
        if "http://posterous.comhttp" in req_url:
            url  = url.split('http://posterous.comhttp')[-1]
            url =  "http%s" % url
        item = Item(response, HTML)
        user = [url for url in hdoc.select_urls('//div[@class="avtr-nm"]//a[contains(@href,"/users")]//h1')]
        user = textify(user).encode('utf8')
        if user:
            item.set('user', user)

        desc = [url for url in hdoc.select_urls('//div[@class="bio"]//p')]
        desc = textify(desc).encode('utf8')
        if desc:
            item.set('desc', desc)

        user_twitter = [url for url in hdoc.select_urls('//li/a[@class="ExtTwitterOauth"]/@href')]
        user_twitter = textify(user_twitter)
        if user_twitter:
            item.set('user_twitter', user_twitter)

        user_flickr = [url for url in hdoc.select_urls('//li/a[@class="ExtFlickr"]/@href')]
        user_flickr =  textify(user_flickr)
        if user_flickr:
            item.set('user_flickr', user_flickr)
        user_knockin = [url for url in hdoc.select_urls('//li/a[@class="ExtMetaWeblog"]/@href')]
        user_knockin = textify(user_knockin)
        if user_knockin:
            item.set('user_knockin', user_knockin)
        user_facebook = [url for url in hdoc.select_urls('//li/a[@class="ExtFacebook"]/@href')]
        user_facebook = textify(user_facebook)
        if user_facebook:
            item.set('user_facebook', user_facebook)

        blog_url = [url for url in hdoc.select_urls('//script[@defer="defer"]')]
        blog_url = textify(blog_url)
        blog_url = re.findall('\"id\":(.*?),',blog_url)
        blog_url = textify(blog_url)
        if blog_url:
            blog_url = "http://posterous.com/api/2/users/%s/sites/public?page=1&per_page=25" % blog_url

        sk = req_url.split('/')[-1]
        item.set('sk',sk)
        yield Request(blog_url, self.parsedict, None, meta={'item':item})


    def parsedict(self,response):
        hxs = HTML(response)
        item = response.meta.get('item')
        data1 = textify(hxs.select('//p')).replace("true", "'true'").replace("false","'false'").replace("null","'null'").replace("url","'url'")
        data1 = eval(data1)
        for data in data1:
            blog_url = data["full_hostname"]
            blog_url = textify(blog_url)
            item.set('blog_url', blog_url)
            subscribe_url = blog_url.split('.')[0]
            subscribe_url = "http://posterous.com/people/subscribers/%s" % subscribe_url
            yield Request(subscribe_url, self.parsenext, None)
        yield item.process()
    def parsenext(self,response):
        hdoc = HTML(response)
        for url in hdoc.select_urls(['//td[@class="name"]//a/@href'],response):
            url = url.replace("people", "users")
            get_page('posterousspace_terminal', url)
        for url in hdoc.select_urls(['//a[@class="next_page"]/@href'],response):
            url =  url
            yield Request(url,self.parsenext,None)
