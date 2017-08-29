from juicer.utils import *

class PlaxoTerminalSpider(JuicerSpider):
    name = 'plaxo_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk',sk)
        item.textify('title', '//span[@class="fn"]')
        item.textify('secondary_info title_line', '//div[@class="secondary_info title_line"]')
        item.textify('secondary_info', '//div[@class="secondary_info"]')
        item.textify('shortdesc secondary_info', '//div[@class="shortDesc secondary_info"]')
        item.textify('workexperience', '//div[@class="experience_title title summary"]//a')
        item.textify('experience_date', '//div[@class="experience_date"]')
        item.textify('experience_description', '//div[@class="experience_description"]')
        item.textify('education_title', '//div[@class="education_title summary"]//a')
        item.textify('education_desc', '//div[@class="education_desc"]//span')
        item.textify('professionalsummary', '//div[@class="aboutMeContent summaryText"]')
        item.textify('profilephoto', '//div[@class="profilePhoto"]//img/@src')
        '''nodes = hdoc.select('//div[@class="experience vevent vcard"]')
        data = {}
        for node in nodes:
            details = []
            experience_title = textify(node.select('.//div[@class="experience_title title summary"]'))
            experience_date = textify(node.select('.//div[@class="experience_date"]'))
            experience_description = textify(node.select('.//div[@class="experience_description"]'))
            details.append(experience_title)
            details.append(experience_date)
            details.append(experience_description)
        item.set('data', data)
        nodes = hdoc.select('//div[@class="searchResultsPerson"]')
        data = {}
        for node in nodes:
            details = []
            name = textify(node.select('.//div[@class="resultsPhoto"]//a'))
            image = textify(node.select('.//div[@class="resultsPhoto"]//a//img/@src'))
            description = textify(node.select('.'))
            details.append(description)
            details.append(image)
            data[name] = details
        item.set('connections', data)
        '''
        yield item.process()
