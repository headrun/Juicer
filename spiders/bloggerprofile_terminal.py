from itertools import chain
from cgi import parse_qs
from juicer.utils import *

from urlparse import urljoin, urlparse

def get_find_url_type(url):
    '''
    http://www.blogger.com/profile-find.g?t=l&loc0=AE (country)
    http://www.blogger.com/profile-find.g?t=l&loc0=QA&loc1=Doha (city)
    http://www.blogger.com/profile-find.g?t=j&ind=TOURISM (industry)
    http://www.blogger.com/profile-find.g?t=o&q=PRO (occupation)
    http://www.blogger.com/profile-find.g?t=i&q=Updating+Technologies (Interest)
    http://www.blogger.com/profile-find.g?t=m&q=Commedy (Movie)
    http://www.blogger.com/profile-find.g?t=s&q=Iniya+Thendral (Music)
    http://www.blogger.com/profile-find.g?t=b&q=Wings+of+Fire (Book)
    '''
    if 'profile-find.g' not in url: return ''

    query = urlparse(url).query
    params = parse_qs(query)

    find_type = params.get('t', [''])[0]

    find_types = {'l': 'location', 'ind': 'industry', 'o': 'occupation',
                  'i': 'interest', 'm': 'movie', 's': 'music', 'b': 'book'}

    find_type = find_types.get(find_type, find_type)
    return find_type

class BloggerProfileTerminalSpider(JuicerSpider):
    name = 'bloggerprofile_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)
        req_url = get_request_url(response)

        item = Item(response, HTML)

        item.textify('name', '//h1')

        attributes = {}
        for tr in hdoc.select("//div[@class='contents-after-sidebar']//tr"):
            key = textify(tr.select(".//th"))
            value = textify(tr.select(".//td"))
            attributes[make_var(key)] = value.strip()

        item.set('attributes', attributes)

        interests = []
        for node in hdoc.select('//span[@class="favorites"]/a'):
            link = textify(node.select('@href'))
            link = urljoin(req_url, link)

            interest = {'term': textify(node), 'type': get_find_url_type(link), 'url': link}
            link = link.split('&ct=')[0]
            get_page('bloggerprofile_browse', link)

            interests.append(interest)

        item.set('interests', interests)

        user_blogs = [textify(blog) for blog in hdoc.select(".//a[contains(@rel, 'contributor-to')]/@href")]
        item.set('user_blogs', user_blogs)

        following_xpath = "//h2[contains(text(), 'Blogs I follow')]/following-sibling::ul/li/a/@href"
        followed_blogs = [textify(i) for i in hdoc.select(following_xpath)]
        item.set('followed_blogs', followed_blogs)

        sk = req_url.split('/')[-1]
        item.set('sk', sk)
        yield item.process()

        for url in hdoc.select_urls('//@href[contains(., "/profile/")]', response):
            url = url.split('&ct=')[0]
            get_page(self.name, url)

