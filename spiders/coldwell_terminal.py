import re
import hashlib
from urlparse import urljoin
from datetime import datetime

from juicer.utils import *

def gen_start_urls():
    items = lookup_items('coldwell_terminal', 'got_page:False', limit=100)
    for _id, term, data in items:
        yield data

def get_sk(url):
    pid = re.findall("propertyId=(.*?)&", url)
    pid = pid[0]
    return pid

def remove_sid(url):
    u = re.findall("(\;jsessionid.*?node[0-9]{2})", url)
    if u:
        url = url.replace(u[0], '')
    return url

class ColdWellBankerTerminalSpider(JuicerSpider):
    name = 'coldwell_terminal'
    start_urls = gen_start_urls() 
    #start_urls = ['http://www.coldwellbanker.com/property?propertyId=183152376&mode=detail&brandType=CB']
    def parse(self, response):
        #import pdb;pdb.set_trace()
        hdoc = HTML(response)
        item = Item(response, HTML)
        url = remove_sid(response.url)
        #sk = hashlib.md5(response.url).hexdigest()
        sk = get_sk(url)
        #item.set('sk', sk)
        #item.set('got_page', True)
        #item.set('url', url)

        street = textify(hdoc.select('//div[@class = "column"]//h3/text()'))
        amount = textify(hdoc.select('//span[@class = "blacktext16bold currencyLink"]/text()'))

        property_detail = {}

        item.set('url',url)
        item.set('sk', sk)
        property_detail['street'] = street
        property_detail['amount'] = amount
        #HOUSE DETAIL
        #no of bedrooms , baths and sqft
        house_stats = hdoc.select('//div[@class = "blacktext14"]//span')
        for stat in house_stats:
            key = textify(stat.select('./text()'))
            key = key.strip()
            key = key.replace(':', '')
            if key:
                value = textify(stat.select('./strong/text()'))
                property_detail[key] = value


        #house id
        hid = textify(hdoc.select('//div[@class = "blacktext14"]/following-sibling::div[1]/span/text()'))
        hid = hid.split(':')
        property_detail['house_id'] = {hid[0].strip():hid[1].strip()}

        #prop details (location, proptype)
        prop_keys = hdoc.select('//span[@class = "propertyDetailLabel"]/text()')
        prop_values = hdoc.select('//span[@class = "propertyDetailContent"]/text()')

        prop_keys = [textify(k) for k in prop_keys]
        prop_values = [textify(v) for v in prop_values]

        prop_keys = [k.strip().replace(':', '') for k in prop_keys]
        prop_values = [v.strip() for v in prop_values]

        if len(prop_keys) == len(prop_values):
            for i in range(len(prop_keys)):
                property_detail[prop_keys[i]] = prop_values[i]

        #description
        prop_desc = textify(hdoc.select('//div[@class = "propertyDescriptionText"]/span/text()'))
        property_detail['description'] = prop_desc


        #features
        f = {}
        features = hdoc.select('//div[@id = "propertyDetailFeatures"]//div[@class = "detailColumnContent blacktext12"]')
        for feature in features:
            key = textify(feature.select('./strong'))
            values = feature.select('.//span')
            values = [textify(v) for v in values]
            #values = [(v.split (':')[0],v.split(':')[1]) for v in values]
            temp = {}
            temp1 = []
            for v in values:
                if ':' in v:
                    temp[v.split(':')[0]] = v.split(':')[1]
                else:
                    temp1.append(v)
            if temp:
                f[key] = temp
            elif temp1:
                f[key] = temp1

        if features:
            property_detail['features'] = f

        #pictures and lat long
        pics = []
        latlong = []
        jscripts = hdoc.select('//script')
        jscripts = [ textify(script) for script in jscripts]
        for script in jscripts:
            pics =  re.findall("addPhoto\(\'(.*?)\'", script)
            latlong = re.findall("propertyDetail.mapLong = (.*?);propertyDetail.mapLat = (.*?);", script)
            if pics and latlong:
                latlong = latlong[0]
                break
        property_detail['pics'] = pics
        property_detail['lat_long'] = latlong

        item.set('details', property_detail)

        #agent info
        agent = {}
        a_info = textify(hdoc.select('//div[@class = "column orangeButton"]//a[contains(@href , "javascript")]/@href'))
        a_info = re.findall("open(.*?)\;", a_info)
        if a_info:
            info = eval(a_info[0])
            agent['name'] = info[3]
            agent['address'] = info[4]
            agent['office_phone'] = info[5]
            agent['cell_phone'] = info[6]
            agent['fax'] = info[7]
            agent['email'] = info[8]
            agent['voice_mail'] = info[9]

        item.set('agent_info', agent)
        item.set('got_page', True)
        yield item.process()

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('got_page:%s' % got_page, item['url'])]




SPIDER = ColdWellBankerTerminalSpider()
