from lxml import etree
from juicer.utils import *
from scrapy.http import FormRequest
from requests.auth import HTTPBasicAuth
import HTMLParser
import requests

class FacebookAricent(JuicerSpider):
    name = "facebook_aricent"
    start_urls = ['https://www.facebook.com/login.php']

    def parse(self,response):
        hdoc = HTML(response)
        formdata={'lsd':'AVpmnhrr',
                    'email':'sravanthi0894@gmail.com',
                    'pass':'sravs@5',
                    'persistent':'',
                    'default_persistent':'1',
                    'timezone':'-330',
                    'lgndim':'eyJ3IjoxMzY2LCJoIjo3NjgsImF3IjoxMzAxLCJhaCI6NzQ0LCJjIjoyNH0=',
                    'lgnrnd':'232813_xkqE',
                    'lgnjs':'1465626493',
                    'locale':'en_GB',
                    'next':'https://www.facebook.com/?stype=lo&jlou=Afcm1q6eMamfGnvEo3nmtJt66CfQMfGAwzr8yCNgIGPvDbfJJEiRNA_xXNJcVXTdkHl0NjpmziLI1iyW_FFSXgD1TxpxnP3AKbsbNVL_YYSX-w&smuh=60666&lh=Ac_bLoFL1jOilqsB',
                    'qsstamp':'W1tbNSwyMSw3NSw4MiwxMDYsMTI1LDEzNSwxNDcsMTg3LDE4OCwyMDQsMjQwLDI1NCwyNzAsMzIzLDMzMCwzMzcsMzM5LDM0OCwzNzIsMzczLDM5NSw0MzMsNDM0LDQ4MSw1MDEsNTQ2LDU3MSw1NzcsNTkzLDYwMCw2MDQsNjExLDYzMSw2MzksNjQwLDY0Myw2NDQsNjU0LDc0OCw5MjYsMTAwN11dLCJBWmx4UEpqZDVLMk5WaTZ3VE1DZmlrdVVraDExXzBZQ0Z0Uk0xSHJsbkFOakJKZ1RIT19PUEdyNnlfQ1lkUGQzWmxNdWJHc2dxMFlrb0hnb0o1V3pxZXNXcXllanhBeVZSUHpwTTl0SEdDZGFvMnBGaWJOSWJVYkl6MVphdXVuanZqNlNTWlFTem9iZVByWXo5WHdYOUNQOWl3VjltX3k5U1NCZFlmSThaeGZhdEd5QTltRjdFSzg2cFVodE01ZFRlTV93NExwXzVTYjBUV3d5V3JHWDBZSkhPeHlkbHJNQVA0RFEyeFB1VFZJU0lRIl0='}
        requests.post(response.url,data=formdata)
        return[FormRequest.from_response(response,formname='login_form',formdata=formdata,callback=self.parse_login,dont_filter=True)]
        #return[FormRequest.from_response(response, formname='login_form', formdata={'email': 'sravanthi0894@gmail.com', 'pass': 'sravs@5', 'cookietime':'on'}, callback=self.parse_login,dont_filter=True)]

    def parse_login(self,response):
        #url = 'https://www.facebook.com/search/122114214480174/likers?ref=about'
        import pdb;pdb.set_trace()
        url = 'https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet?dpr=1&data=%7B%22typeahead_sid%22%3A%22%22%2C%22tr%22%3Anull%2C%22reaction_surface%22%3Anull%2C%22topic_id%22%3Anull%2C%22em%22%3Afalse%2C%22reaction_session_id%22%3Anull%2C%22mr%22%3Afalse%2C%22view%22%3A%22list%22%2C%22display_params%22%3A[]%2C%22logger_source%22%3A%22www_main%22%2C%22encoded_query%22%3A%22%7B%5C%22bqf%5C%22%3A%5C%22likers(122114214480174)%5C%22%2C%5C%22vertical%5C%22%3A%5C%22none%5C%22%2C%5C%22post_search_vertical%5C%22%3Anull%2C%5C%22intent_data%5C%22%3Anull%2C%5C%22filters%5C%22%3A[]%2C%5C%22has_chrono_sort%5C%22%3Afalse%2C%5C%22query_analysis%5C%22%3Anull%2C%5C%22subrequest_disabled%5C%22%3Afalse%7D%22%2C%22trending_source%22%3Anull%2C%22has_top_pagelet%22%3Atrue%2C%22ref_path%22%3A%22%2Fsearch%2F122114214480174%2Flikers%22%2C%22tl_log%22%3Afalse%2C%22encoded_title%22%3A%22WyJQZW9wbGUrd2hvK2xpa2UrIix7InRleHQiOiJBcmljZW50IiwidWlkIjoxMjIxMTQyMTQ0ODAxNzQsInR5cGUiOiJwYWdlIn1d%22%2C%22is_trending%22%3Afalse%2C%22page_number%22%3A6%2C%22browse_location%22%3A%22%22%2C%22place_id%22%3Anull%2C%22filter_ids%22%3A%7B%221581495710%22%3A1581495710%2C%22100000130263107%22%3A100000130263107%2C%22100001556674502%22%3A100001556674502%7D%2C%22callsite%22%3A%22browse_ui%3Ainit_result_set%22%2C%22cursor%22%3A%22AbqgTznQoXhFSwf8t4H3jv3wwk4gtnr1n5sNBUfbdRcmoHnnFy5wQEsNhtwGDD9tW4J5Bd484V6jWlDyhMYcAVmZub7AaTdxE62xWT0ToP07b964cVXaMBmZa1wfPUtXQSXLd58yErv0dgC1Eb2hTKmT_uj2hQZzbleRMl1sq6HMk9jyUiGHkIwMxv0JrINHAGiFWXB_Y4I4bAPtRyYztl4THRH-f2O2VfETwNEwADd6CVketlt5aPnC5g-RCrhW--vFtwrE4lxbgID8UFJd9Kj0jQMe5I8Pm0H9LsJrOD-8KzaTXTbQMkbfGWKIPps6wZ0%22%2C%22exclude_ids%22%3Anull%2C%22impression_id%22%3A%22288cfc41%22%2C%22ref%22%3A%22about%22%2C%22experience_type%22%3A%22grammar%22%2C%22story_id%22%3Anull%7D&__user=100011743200084&__a=1&__dyn=7AmajEzURoG649UoHaEWC5ECiq2W8GAdy8VFLO0xBxCbzES2N6y8-bxu13wHgf8vkwy3fgjx2FbDG4UpxicxW3ucDyU9XxCFEW2PxOcxu5ocE88C9z9pqyU&__req=k&__be=0&__pc=EXP1%3ADEFAULT&__rev=2336846'
        yield Request(url,self.parse_next,response)


    def parse_next(self,response):
        data = response.body.replace('for (;;);','').replace('\u003C','<').replace('\/','/')#.replace('&#123;','{').replace('&#125;','}').replace('&quot;','"').replace('\\','')
        import pdb;pdb.set_trace()
        null=''
        false=''
        true=''
        data=eval(data)
        i = HTMLParser.HTMLParser()
        x=str(i.unescape(data['jsmods']))
        i=i.unescape(data['payload'])
        cursor = textify(re.findall('cursor(.*?),', x)).strip("': '")
        pg_number = textify(re.findall('page_number(.*?)\,',x)).strip("': ")
        data = etree.HTML(i)
        try:
            count = response.meta['count']
        except:count = []
        threads = data.xpath('//div[@class="_3u1 _gli _5und"]')
        for thread in threads:
            name = textify(thread.xpath('.//div[@class="_5d-5"]/text()'))
            link = thread.xpath('.//div[@class="_gll"]/a/@href')
            link = thread.xpath('.//div[@class="_gll"]/a/@href')
            location = thread.xpath('.//div[contains(text(),"Lives in")]/a/text()')
            other_info = thread.xpath('.//div[@class="_glj"]//div[@class="_glm"]//text()')
            info = thread.xpath('.//div[@class="_glj"]//div[@class="_glo"]//text()')
            count.append(name)

        nxt_pg ='https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet?dpr=1&data=%7B%22typeahead_sid%22%3A%22%22%2C%22tr%22%3Anull%2C%22reaction_surface%22%3Anull%2C%22topic_id%22%3Anull%2C%22em%22%3Afalse%2C%22reaction_session_id%22%3Anull%2C%22mr%22%3Afalse%2C%22view%22%3A%22list%22%2C%22display_params%22%3A[]%2C%22logger_source%22%3A%22www_main%22%2C%22encoded_query%22%3A%22%7B%5C%22bqf%5C%22%3A%5C%22likers(122114214480174)%5C%22%2C%5C%22vertical%5C%22%3A%5C%22none%5C%22%2C%5C%22post_search_vertical%5C%22%3Anull%2C%5C%22intent_data%5C%22%3Anull%2C%5C%22filters%5C%22%3A[]%2C%5C%22query_analysis%5C%22%3Anull%2C%5C%22subrequest_disabled%5C%22%3Afalse%7D%22%2C%22trending_source%22%3Anull%2C%22has_top_pagelet%22%3Atrue%2C%22ref_path%22%3A%22%2Fsearch%2F122114214480174%2Flikers%22%2C%22tl_log%22%3Afalse%2C%22encoded_title%22%3A%22WyJQZW9wbGUrd2hvK2xpa2UrIix7InRleHQiOiJBcmljZW50IiwidWlkIjoxMjIxMTQyMTQ0ODAxNzQsInR5cGUiOiJwYWdlIn1d%22%2C%22is_trending%22%3Afalse%2C%22page_number%22%3A' + pg_number + '%2C%22browse_location%22%3A%22%22%2C%22filter_ids%22%3A%7B%22100004739290605%22%3A100004739290605%2C%22100003230106131%22%3A100003230106131%7D%2C%22callsite%22%3A%22browse_ui%3Ainit_result_set%22%2C%22cursor%22%3A%22' + cursor + '%22%2C%22exclude_ids%22%3Anull%2C%22impression_id%22%3A%224d3d015e%22%2C%22ref%22%3A%22about%22%2C%22experience_type%22%3A%22grammar%22%2C%22story_id%22%3Anull%7D&__user=100011743200084&__a=1&__dyn=7AmajEzURoG649UoGya4A5EWq2W8GAdy8Z9LO0xBxCbzES2N6y8-bxu13wFQ3O7R88y8aJxa4aAKuEjxC267E4iubwDK4VqCzEbe78O5UlwOwww&__req=j&__pc=EXP1%3ADEFAULT&__rev=2256867'
        print len(count)
