from itertools import chain
from cgi import parse_qs
from juicer.utils import *

from urlparse import urljoin, urlparse


class PosterousProfileTerminalSpider(JuicerSpider):
    name = 'posterousprofile_terminal'
    def parse(self, response):
        hdoc = HTML(response)
        req_url = get_request_url(response)
        got_page(self.name, response)
        item = Item(response, HTML)
        user = [url for url in hdoc.select_urls('//div[@class="avtr-nm"]//a[contains(@href,"/users")]//h1')]
        user = textify(user).encode('utf8')
        if user:
            item.set('user', user)
        desc = [url for url in hdoc.select_urls('//div[@class="bio"]//p')]
        desc = textify(desc).encode('utf8')
        if desc:
            item.set('desc', desc)
        
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
            get_page('posterousprofile_browse', subscribe_url)
        yield item.process()
