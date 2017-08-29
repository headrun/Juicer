from juicer.utils import *

class Country_codes(JuicerSpider):
    name = 'country_codes'
    start_urls = ['http://www.iso.org/iso/iso-3166-1_decoding_table.htmllist']

    def parse(self, response):
        hdoc = HTML(response)

        nodes = hdoc.select('//table[@id="country_codes"]/tbody/tr')
        for node in nodes:
            code = textify(node.select('./td[@data-label="Code"]')).encode('utf8').decode('ascii','ignore')
            country = textify(node.select('./td[@data-label="Country name"]')).encode('utf8').decode('ascii','ignore')
            status = textify(node.select('./td[@data-label="Status"]')).encode('utf8').decode('ascii','ignore')
            print 'code>>>>>>', code , country, status
            out_file = file('/home/headrun/country_codes','ab+')
            out_file.write('%s\t%s\t%s\n' %(code,country,status))
            out_file.close()
