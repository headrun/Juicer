from juicer.utils import *

class Facebook(JuicerSpider):
    name = 'facebook_pages'
    start_urls = [
        'https://www.facebook.com/directory/pages/I',
        'https://www.facebook.com/directory/pages/K',
        'https://www.facebook.com/directory/pages/U',
        'https://www.facebook.com/directory/pages/W'
    ]

    def parse(self, response):
        #got_page(self.name, response)
        hdoc = HTML(response)

        pages = hdoc.select_urls(['//div[@class="UIFullPage_Container"]/div[1]/\
                table[@class="uiGrid _51mz mam"]//div[@class="clearfix"]/a/@href'], response)

        for page in pages:
            if 'india' in page.lower():
                print 'indian_fb_page>>>', page
                get_page('facebook_pages', page)

        directories = hdoc.select('//div[@class="UIFullPage_Container"]/div[2]//li[@class="fbDirectoryBoxColumnItem"]/a/text()')
        for directory in directories:
            directory = textify(directory)
            if 'india' in directory.lower():
                print 'indian_pages_dir>>>', directory
                get_page(self.name, directory)
