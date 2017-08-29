from time import strftime, gmtime, sleep
from urllib2 import quote
from hashlib import sha1
from base64 import b64encode
import hmac
import datetime


args = {}
args['AWSAccessKeyId']= 'AKIAJSFJSHY3WVKBFQDQ'
args['Action'] = 'TrafficHistory'
args['SignatureVersion'] = '2'
args['SignatureMethod'] = 'HmacSHA256'
args['Timestamp'] = datetime.datetime.now().isoformat()
args['Url'] = 'www.aricent.com'
args['ResponseGroup'] = 'History'
keys = args.keys()

_args = '&'.join('%s=%s' % (key, quote(unicode(args[key]).encode('utf-8'), safe='~')) for key in keys)

msg = 'GET'
msg += '\n' + 'awis.amazonaws.com'
msg += '\n/'
msg += '\n' + _args
signature = quote(b64encode(hmac.new('ia/rDmn6oIhG63+cqG0sAoa+cJpCOeOCU7wtNM5M',msg, sha1).digest()))
url = 'http://awis.amazonaws.com/?Action=TrafficHistory&AWSAccessKeyId=AKIAJNOXRRVQMFCD2RFQ&Signature=%s&SignatureMethod=HmacSHA1&SignatureVersion=2&Timestamp=%s&Url=www.aricent.com&ResponseGroup=History'%(signature,args['Timestamp'])
#url = 'http://%s/?%s&Signature=%s'%('awis.amazonaws.com',_args,signature)
print url
