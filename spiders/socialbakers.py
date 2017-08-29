from juicer.utils import *
import MySQLdb

class Socialbakers(JuicerSpider):
    name = 'socialbakers'

    def start_requests(self):
        req = []

        countries = ['afghanistan', 'aland-islands', 'albania', 'algeria', 'american-samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua-and-barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire,-saint-eustatius-and-saba-', 'bosnia-and-herzegovina', 'botswana', 'bouvet-island', 'brazil', 'british-indian-ocean-territory', 'british-virgin-islands', 'brunei', 'bulgaria', 'burkina-faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape-verde', 'cayman-islands', 'central-african-republic', 'chad', 'chile', 'china', 'christmas-island', 'cocos-islands', 'colombia', 'comoros', 'cook-islands', 'costa-rica', 'croatia', 'cuba', 'curacao', 'cyprus', 'czech-republic', 'democratic-republic-of-the-congo', 'denmark', 'djibouti', 'dominica', 'dominican-republic', 'east-timor', 'ecuador', 'egypt', 'el-salvador', 'equatorial-guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland-islands', 'faroe-islands', 'fiji', 'finland', 'france', 'french-guiana', 'french-polynesia', 'french-southern-territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard-island-and-mcdonald-islands', 'honduras', 'hong-kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle-of-man', 'israel', 'italy', 'ivory-coast', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall-islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands-antilles', 'new-caledonia', 'new-zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk-island', 'northern-mariana-islands', 'north-korea', 'norway', 'oman', 'pakistan', 'palau', 'palestinian-territory', 'panama', 'papua-new-guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto-rico', 'qatar', 'republic-of-the-congo', 'reunion', 'romania', 'russia', 'rwanda', 'saint-barthelemy', 'saint-helena', 'saint-kitts-and-nevis', 'saint-lucia', 'saint-martin', 'saint-pierre-and-miquelon', 'saint-vincent-and-the-grenadines', 'samoa', 'san-marino', 'sao-tome-and-principe', 'saudi-arabia', 'senegal', 'serbia', 'serbia-and-montenegro', 'seychelles', 'sierra-leone', 'singapore', 'sint-maarten', 'slovakia', 'slovenia', 'solomon-islands', 'somalia', 'south-africa', 'south-georgia-and-the-south-sandwich-islands', 'south-korea', 'south-sudan', 'spain', 'sri-lanka', 'sudan', 'suriname', 'svalbard-and-jan-mayen', 'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tokelau', 'tonga', 'trinidad-and-tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks-and-caicos-islands', 'tuvalu', 'uganda', 'ukraine', 'united-arab-emirates', 'united-kingdom', 'united-states', 'united-states-minor-outlying-islands', 'uruguay', 'u.s.-virgin-islands', 'uzbekistan', 'vanuatu', 'vatican', 'venezuela', 'vietnam', 'wallis-and-futuna', 'western-sahara', 'yemen', 'zambia', 'zimbabwe'
            ]

        countries = ['pakistan']
        category_urls = ['http://www.socialbakers.com/facebook-pages/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/brands/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/media/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/entertainment/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/sport/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/society/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/community/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/celebrities/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/place/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/politics/country/%s/',
                    ]

        countries_completed = ["india", "singapore", "malaysia", "indonesia",
                                "philippines", "china", "vietnam", "thailand", "united-states"
                        ]

        for country in countries:
            if country in countries_completed:
                continue
            for category_url in category_urls:
                con_url = category_url %(country)
                category = category_url.split('/')[-4]
                print "category>>>", category
                r = Request(con_url, self.parse, None, meta = {'country' : country, 'category' : category})
                req.extend(r)


        return req

    def parse(self, response):
        hdoc = HTML(response)

        category = response.meta['category']
        country = response.meta['country']

        pages = hdoc.select('//section[@class="content"]//td[@class="rank"]/following-sibling::td[1]/a')
        for page in pages:
            social_bakers_url = textify(page.select('./@href'))
            title = textify(page.select('.//text()')).encode('utf8').decode('ascii','ignore')
            fb_page_id = ''.join(re.findall(r'\d+', social_bakers_url))
            fb_page = 'https://www.facebook.com/%s' %(fb_page_id)
            feed_url = 'https://www.facebook.com/feeds/page.php?id=%s&format=rss20' %(fb_page_id)

            try:
                conn = MySQLdb.connect(host='127.0.0.1', user='root', db='socialbakers', passwd='root')
                cursor = conn.cursor()
                query = "insert into socialbakers_urls(fb_page_id,country,category,page_title,feed_url,social_bakers_url,created_at,modified_at) values(%s,%s,%s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now()"
                values = (str(fb_page_id),str(country),str(category), str(title),str(feed_url),str(social_bakers_url))
                cursor.execute(query,values)
                cursor.close()
            except Exception as e:
                print e.message

        next_page = textify(hdoc.select('//li[@class="next"]/a/@href'))
        if next_page:
            next_page = 'http://www.socialbakers.com' + next_page
            yield Request(next_page, self.parse, meta = {"country" : country, "category": category})

