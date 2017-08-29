from juicer.utils import *
#import MySQLdb

class Socialbakers(JuicerSpider):
    name = 'socialbakers'

    def start_requests(self):
        req = []

        countries = ['afghanistan', 'aland-islands', 'albania', 'algeria', 'american-samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua-and-barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire,-saint-eustatius-and-saba-', 'bosnia-and-herzegovina', 'botswana', 'bouvet-island', 'brazil', 'british-indian-ocean-territory', 'british-virgin-islands', 'brunei', 'bulgaria', 'burkina-faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape-verde', 'cayman-islands', 'central-african-republic', 'chad', 'chile', 'china', 'christmas-island', 'cocos-islands', 'colombia', 'comoros', 'cook-islands', 'costa-rica', 'croatia', 'cuba', 'curacao', 'cyprus', 'czech-republic', 'democratic-republic-of-the-congo', 'denmark', 'djibouti', 'dominica', 'dominican-republic', 'east-timor', 'ecuador', 'egypt', 'el-salvador', 'equatorial-guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland-islands', 'faroe-islands', 'fiji', 'finland', 'france', 'french-guiana', 'french-polynesia', 'french-southern-territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard-island-and-mcdonald-islands', 'honduras', 'hong-kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle-of-man', 'israel', 'italy', 'ivory-coast', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall-islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands-antilles', 'new-caledonia', 'new-zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk-island', 'northern-mariana-islands', 'north-korea', 'norway', 'oman', 'pakistan', 'palau', 'palestinian-territory', 'panama', 'papua-new-guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto-rico', 'qatar', 'republic-of-the-congo', 'reunion', 'romania', 'russia', 'rwanda', 'saint-barthelemy', 'saint-helena', 'saint-kitts-and-nevis', 'saint-lucia', 'saint-martin', 'saint-pierre-and-miquelon', 'saint-vincent-and-the-grenadines', 'samoa', 'san-marino', 'sao-tome-and-principe', 'saudi-arabia', 'senegal', 'serbia', 'serbia-and-montenegro', 'seychelles', 'sierra-leone', 'singapore', 'sint-maarten', 'slovakia', 'slovenia', 'solomon-islands', 'somalia', 'south-africa', 'south-georgia-and-the-south-sandwich-islands', 'south-korea', 'south-sudan', 'spain', 'sri-lanka', 'sudan', 'suriname', 'svalbard-and-jan-mayen', 'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tokelau', 'tonga', 'trinidad-and-tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks-and-caicos-islands', 'tuvalu', 'uganda', 'ukraine', 'united-arab-emirates', 'united-kingdom', 'united-states', 'united-states-minor-outlying-islands', 'uruguay', 'u.s.-virgin-islands', 'uzbekistan', 'vanuatu', 'vatican', 'venezuela', 'vietnam', 'wallis-and-futuna', 'western-sahara', 'yemen', 'zambia', 'zimbabwe'
            ]

        category_urls = ['http://www.socialbakers.com/statistics/facebook/pages/total/%s/brands/',
                        'http://www.socialbakers.com/statistics/facebook/pages/total/%s/celebrities/',
                        'http://www.socialbakers.com/statistics/facebook/pages/total/%s/community/',
                        'http://www.socialbakers.com/statistics/facebook/pages/total/%s/entertainment/',
                        'http://www.socialbakers.com/statistics/facebook/pages/total/%s/media/',
                        'http://www.socialbakers.com/statistics/facebook/pages/total/%s/place/',
                        'http://www.socialbakers.com/statistics/facebook/pages/total/%s/society/',
                        'http://www.socialbakers.com/statistics/facebook/pages/total/%s/sport/'
                        ]

        countries_completed = ["philippines", "united-states", "india"
                        ]

        #for country in countries:
        for country in countries_completed[:1]:
            for category_url in category_urls:
                con_url = category_url %(country)
                category = category_url.split('/')[-2]
                r = Request(con_url, self.parse, None, meta = {'country' : country, 'category' : category})
                req.extend(r)

        return req

    def parse(self, response):
        hdoc = HTML(response)
        category = response.meta['category']
        country = response.meta['country']

        pages = hdoc.select('//div[@class="item"]/a/@href').extract()
        for page in pages:
            if 'http' not in page: page = 'http://www.socialbakers.com' + page
            yield Request(page,self.parse_next,response,meta={'country' : country, 'category' : category})

        next_page = textify(hdoc.select('//div[@class="more-center-link"]/a[@rel="next"]/@href'))
        if next_page:
            next_page = 'http://www.socialbakers.com' + next_page
            yield Request(next_page, self.parse, meta = {"country" : country, "category": category})

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="account"]/text()'))
        fans = textify(hdoc.select('//div[contains(text(),"Number of Fans")]/following-sibling::strong/text()'))
        fans = ''.join(re.findall('\d+',fans))
        facebook_page = textify(hdoc.select('//a[@class="blank show-tooltip"]/@href'))
        fb_id = textify(hdoc.select('//div/@data-page-id'))
        were_herecount = textify(hdoc.select('//div[contains(text(),"Were Here Count")]/following-sibling::strong/text()'))
        name = textify(hdoc.select('//a[@class="blank show-tooltip"]/text()')) or textify(hdoc.select('//a[@data-tooltip]/abbr/@data-tooltip'))
        other_info = hdoc.select('//div[@class="account-tag-list"]//li/a/text()').extract()
        fans_byday = textify(hdoc.select('//strong[@class="interval-day growth"]/text()')) or textify(hdoc.select('//strong[@class="interval-day loss"]/text()'))
        fans_byweek = textify(hdoc.select('//strong[@class="interval-week growth"]/text()')) or textify(hdoc.select('//strong[@class="interval-week loss"]/text()'))
        fans_bymonth = textify(hdoc.select('//strong[@class="interval-month growth"]/text()')) or textify(hdoc.select('//strong[@class="interval-month loss"]/text()'))
        country = response.meta['country']
        category = response.meta['category']
        author = {'name':xcode(name),'url':facebook_page}
        edit_tags = []

        file_name = country + "socialbakers_data"
        file_name = "/home/headrun/kiran/juicer/trunk/juicer/spiders/" + file_name
        fans_daybyday = {'daily':fans_byday,'weekly':fans_byweek,'monthly':fans_bymonth}
        for info in other_info:
            info = str(info.strip('\n\t'))
            if info != '':edit_tags.append(info)

        print category

        out_file = file(file_name, 'ab+')
        out_file.write('url:%s,title:%s,author:%s,fans_count:%s,fans_daybyday:%s,country:%s,category:%s,fb_id:%s,edit_tags:%s\n'%(response.url,xcode(title),xcode(author),xcode(fans),fans_daybyday,xcode(country),category,fb_id,xcode(edit_tags)))
        #out_file.write('https://www.facebook.com/feeds/page.php?id=%s&format=rss20,%s\n'%(fb_id,fb_id))
        out_file.close()
