from juicer.utils import *

class SpiderCrunchBase(JuicerSpider):
    name = 'crunchbase_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        # Add Reqd code
        sk=response.url.split("/")[-1]
        item.textify("company_name","//div[@id=\"breadcrumbs\"]/span[2]")
        item.textify("category","//td[string(@class)=\"td_left\" and contains(string(.),\"Category\")]/following-sibling::td[1]")
        item.textify("description","//div[@id=\"col2_internal\"]/p")

        email = textify(hdoc.select('//script[contains(., "unescape")]'))
        email = email.split("unescape('")[-1].split("'))")[0]
        email = ''.join([chr(eval('0x' + email[i+1:i+3])) for i in xrange(0, len(email), 3)]).split('mailto:')[-1].split('"')[0]

        yield item.set_many({'sk': sk, 'email': email}).process()
        got_page(self.name, response)
