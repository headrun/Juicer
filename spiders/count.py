import sys
import time

from cloudlibs import proxy

def main(domain):

    db = proxy('http://api.cloudlibs.com/db/', '4e8d4f84df3cb5386a000005')
    result = db.base.login('karthik.reddi', 'hdrn59!')
    db.set('session_key', result['result']['session_key'])

    data = db.count('juicerprod', 'rss', spec={'url':{'$regex':domain}})
    import pdb;pdb.set_trace()
    results = db.find('juicerprod', 'rss', spec={'url':{'$regex':domain}}, limit=data['result'])

    results = results['result']
    print 'url_hash', '\t\t', 'last_run', '\t\t', 'next_run', '\t\t', 'diff in mins', '\t\t', 'url'
    for r in results:
        last_run = parser.parse(time.ctime(r['last_run'])).strftime('%Y-%m-%dT%H:%M')
        next_run = parser.parse(time.ctime(r['next_run'])).strftime('%Y-%m-%dT%H:%M')
        diff = (r['next_run'] - r['last_run'])/60
        print r['url_hash'], '\t',  last_run, '\t', next_run, '\t', diff, '\t', r['url']

if __name__ == '__main__':
    main(sys.argv[1])
