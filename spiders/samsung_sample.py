import urllib
data = urllib.urlopen("http://webhose.io/search?token=80dc0f94-8879-408e-b92a-c55416082c69&format=json&q=LG&ts=1450527612000&size=100&country=NZ&site_type=blogs").read()
import json
dat = json.loads(data)
for i in dat["posts"]:
    s = i["thread"]
    print s["site_section"]
    
