from juicer.utils import*
from dateutil import parser

class practise(juicerspider):
    name = 'practise1'
    start_urls = ['http://makassarterkini.com/']

    def parse(self, response):
    hdoc = HTML(response)
    category_links = hdoc.select('//li[contains(@id, "menu-item-")]/a/@href')
    for link in category_links:
       yield Request(link, self.parse)
    
    rss_link = textify(hdoc.select('//a[@class="rss-cat-icon ttip"]/@href'))
    f = open("rss_links.text", "a")
    f.write(rss_link)
    f.write("\n")

