from juicer.utils import *
from scrapy.http import FormRequest

class Facebooksample(JuicerSpider):
    name = 'sample_fb'
    start_urls = ['https://www.facebook.com']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        url = 'https://www.facebook.com/login.php?login_attempt=1&lwv=110'
        headers = {':authority':'www.facebook.com',
                    ':method':'GET',
                    ':path':'/?stype=lo&jlou=Afe8QG4B06AaPaVJI95jVUFc3lx7l4Yye5NJNM7vzeyTyNMjwiP54Em_4MIVLMs1PrYJzVv8z8IjSkQfhKKIg9VYgEnYjWo_MUJ_TMm9HVzO0A&smuh=60666&lh=Ac9TnpJRwC0ESP8R',
                    "scheme":"https",
                    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "accept-encoding":"gzip, deflate, sdch",
                    "accept-language":"en-US,en;q=0.8",
                    "cache-control":"no-cache",
                    'cookie':'datr=53bBVpuTzfqA3g8e3Q2zYiqk; locale=en_GB; sb=y8MVVxCUnJPgjRGmCd98BGAn; c_user=100011743200084; xs=28%3AXwLTr1DmT41GYQ%3A2%3A1465627844%3A-1; csm=2; s=Aa5l7q9UID4bOyBs.BXW7TE; pl=n; lu=ggMQ_enwb049wjk8pJaMr1kA; p=-2; presence=EDvF3EtimeF1465628100EuserFA21B117432B84A2EstateFDt2F_5b_5dElm2FnullEuct2F1465627245BEtrFnullEtwF1986503095EatF1465628040554G4656281B56CEchFDp_5f1B117432B84F3CC; fr=0vwdCFFzJTbIyfJrI.AWU887vuS2kJz8TrI38xRLIuSQo.BXFcPM._2.Fdb.0.0.AWWJLbJJ; wd=1366x449',
                    'pragma':'no-cache',
                    'referer':'https://www.facebook.com/?stype=lo&jlou=Afe8QG4B06AaPaVJI95jVUFc3lx7l4Yye5NJNM7vzeyTyNMjwiP54Em_4MIVLMs1PrYJzVv8z8IjSkQfhKKIg9VYgEnYjWo_MUJ_TMm9HVzO0A&smuh=60666&lh=Ac9TnpJRwC0ESP8R',
                    'upgrade-insecure-requests':'1',
                    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'}
        form_data = {'lsd':'AVpmnhrr',
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
        yield FormRequest(response.url, callback=self.parse_url, formdata=form_data, dont_filter=True,headers=headers)


    def parse_url(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
