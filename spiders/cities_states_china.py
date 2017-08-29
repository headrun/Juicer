from juicer.utils import *
import urllib

class Wiki(JuicerSpider):
    name = 'cities_states_china'
    start_urls = ['http://en.wikipedia.org/wiki/List_of_cities_in_China']

    def parse(self, response):
        hdoc = HTML(response)
        _nodes = hdoc.select('//table[contains(@class,"wikitable sortable")]')
        nodes = _nodes.select('.//tr//a[contains(@href,"/wiki/")]/ancestor::tr')
        for node in nodes[1:]:
            _nodes = node.select('.//td')
            city = textify(_nodes[0].select('.//text()'))
            chinese_city_name = textify(_nodes[1].select('.//text()')).encode('utf8')
            province = textify(_nodes[2].select('.//text()'))
            if '19' in province:
                province = ''

            print city, '\t', str(chinese_city_name), '\t', province
            country = 'china'

            url = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %(province,city)
            url1 = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %(province, urllib.quote(chinese_city_name))
            url2 = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %(province, '')
            url3 = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %(city, '')
            url4 = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %(urllib.quote(chinese_city_name), '')
            url5 = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %('', city)
            url6 = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %('', urllib.quote(chinese_city_name))
            url7 = 'https://www.blogger.com/profile-find.g?t=l&loc0=CN&loc1=%s&loc2=%s' %('', province)

            get_page('blogger_urls_cn', url)
            get_page('blogger_urls_cn', url1)
            get_page('blogger_urls_cn', url2)
            get_page('blogger_urls_cn', url3)
            get_page('blogger_urls_cn', url4)
            get_page('blogger_urls_cn', url5)
            get_page('blogger_urls_cn', url6)
            get_page('blogger_urls_cn', url7)
