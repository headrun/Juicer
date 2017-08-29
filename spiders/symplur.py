from juicer.utils import *

class Symplur(JuicerSpider):
    name = "symplur"
    start_urls = ["http://www.symplur.com/healthcare-hashtags/regular/",
                  "http://www.symplur.com/healthcare-hashtags/tweet-chats/",
                  "http://www.symplur.com/healthcare-hashtags/conferences/",
                  "http://www.symplur.com/healthcare-hashtags/diseases/",
                  "http://www.symplur.com/healthcare-hashtags/ontology/cancer/"
            ]

    def parse(self, response):
        hdoc = HTML(response)

        hashtags = hdoc.select('//div[@id="content"]//a[contains(@href,"healthcare-hashtags")]')

        hashtags = [textify(i.select('./text()')) for i in hashtags]
        hashtags = [tag.strip() for tag in hashtags if "#" in tag]
        category = response.url.split("/")[-2]
        if category == "cancer":
            category = "ontology_cancer"

        category = "healthcare_hashtags_" + category
        file_path = "/home/headrun/venu/pharma/%s" %(category)

        outfile = file(file_path, "ab+")
        for hashtag in hashtags:
            outfile.write("%s\n" %(hashtag))

        outfile.close()
