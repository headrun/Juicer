from time import strftime, gmtime, sleep
from urllib2 import quote
from hashlib import sha256
from base64 import b64encode
import hmac

args = {}
args['AWSAccessKeyId'] = 'AKIAJ56ZUJFGZXPXK3UQ'
args['Service'] = 'AWSECommerceService'
args['Version'] = '2011-08-01'
args['Operation'] = 'BrowseNodeLookup'
args['AssociateTag'] = 'FOO'
args['BrowseNodeId'] = '1063498'
args['ResponseGroup'] = 'NewReleases,TopSellers'
args['Timestamp'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
args['Timestamp'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
keys = sorted(args.keys())

_args = '&'.join('%s=%s' % (key, quote(unicode(args[key]).encode('utf-8'), safe='~')) for key in keys)

msg = 'GET'
msg += '\n' + 'ecs.amazonaws.com'
msg += '\n/onca/xml'
msg += '\n' + _args
signature = quote(b64encode(hmac.new('b1LDye7n8eDAaRC1/FLUOSWijmq15iz+JKIlHIqs', msg, sha256).digest()))
url = 'http://%s/onca/xml?%s&Signature=%s' % ('ecs.amazonaws.com', _args, signature)
print url
