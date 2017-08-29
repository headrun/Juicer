import feedparser

def main():
    data = feedparser.parse('http://data.alexa.com/data?cli=10&dat=json&url=www.aricent.com')
    country_details = {str(data['feed']['country']['name']):str(data['feed']['country']['rank'])}
    Global_rank = str(data['feed']['popularity']['text'])
    print 'country_details',country_details
    print 'Global_rank',Global_rank

main()
