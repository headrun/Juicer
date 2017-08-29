import sys
	
import csv
import json
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(fb_laos_pgid):
    f = open(fb_laos_pgid,'rb+')
    s = csv.reader(f)
    output_file = 'my_fb_location'
    for row in s:
        url = "https://graph.facebook.com/v2.8/%s/?access_token=EAACEdEose0cBACZCdpU6fqzJjrjeJwu9LuaY5K3ZCZBCu4lrP6kHueDjpUNQLesMrMa7beZA00znasUdtNoQW5zdljB9NOMx1MlGZA6D9TVkZBZAHeKtkYZBUtTDxIAZCstXyDTsZCkZAO4Sc8fDJfD0x29c8HI5idUZCrGero5aAdZAe9jZCOor22rxYR&fields=location"%row[0]
        page = "https://www.facebook.com/feeds/page.php?id=%s&format=rss20"%row[0]
        try:response = json.loads(urllib2.urlopen(url).read()).get('location')
        except:
            print row
            continue
        if response: 
            data = response.get('country') or response.get('city')
        else: data = ''
        out_file = file(output_file,'ab+')
        out_file.write('%s#<>#%s#<>#%s\n'%(page ,row[0], data))

main('fb_laos_pgid')
