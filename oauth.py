import time, random
import urllib, urllib2
import hmac, hashlib
import cgi

# Consumer Key
ckey = "3vqTk4hvNAno7NGzgBpdg"
# Consumer Secret
csecret = "PaeZx823Laxz3L5OF1R32zk9klW92tVyqn5mXjAoIw"

def make_signature(params, url, csecret, secret = ""):
    # Generate Signature Base String
    plist = []
    for i in sorted(params):
        plist.append("%s=%s" % (i, params[i]))

    pstr = "&".join(plist)
    msg = "GET&%s&%s" % (
        urllib.quote(url, ""), urllib.quote(pstr, ""))

    # Calculate Signature
    h = hmac.new("%s&%s" % (csecret, secret), msg, hashlib.sha1)
    sig = h.digest().encode("base64").strip()
    
    return sig

def init_params():
    p = {
        "oauth_consumer_key": ckey,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": str(random.getrandbits(64)),
        "oauth_version": "1.0"
        }

    return p

# Request Token URL
reqt_url = 'http://twitter.com/oauth/request_token'
# Authorize URL
auth_url = 'http://twitter.com/oauth/authorize'
# Access Token URL
acct_url = 'http://twitter.com/oauth/access_token'
# status update
post_url = 'http://twitter.com/statuses/update.xml'
# acount verify_credentials
avfy_url = 'http://twitter.com/account/verify_credentials.xml'
# show friends timeline
frtl_url = 'http://twitter.com/statuses/friends_timeline.xml'

# Request Parameters
params = init_params()

print "Get request token:",

# Generate Signature
sig = make_signature(params, reqt_url, csecret)
params["oauth_signature"] = sig

# Get Token
req = urllib2.Request("%s?%s" % (reqt_url, urllib.urlencode(params)))
resp = urllib2.urlopen(req)

print "\t[OK]"

# Parse Token Parameters
ret = cgi.parse_qs(resp.read())
token = ret["oauth_token"][0]
token_secret = ret["oauth_token_secret"][0]

print "* Please access to this URL, and allow."
print "> %s?%s=%s" % (auth_url, "oauth_token", token)
print "\n* After that, will display 7 digit PIN, input here."
print "PIN ->",
pin = raw_input()
pin = int(pin)

print "Get access token:",

params = init_params()
params["oauth_verifier"] = pin
params["oauth_token"] = token

sig = make_signature(params, acct_url, csecret, token_secret)
params["oauth_signature"] = sig

req = urllib2.Request("%s?%s" % (acct_url, urllib.urlencode(params)))
resp = urllib2.urlopen(req)

print "\t[OK]"

fin = cgi.parse_qs(resp.read())
atoken = fin["oauth_token"][0]
atoken_secret = fin["oauth_token_secret"][0]

print "Your screen_name is '%s'." % fin["screen_name"][0]

print "What are you doing?:",
post = raw_input()

params = init_params()
params["oauth_token"] = atoken
params["status"] = post.decode("utf-8")

sig = make_signature(params, post_url, csecret, atoken_secret)
params["oauth_signature"] = sig

req = urllib2.Request(post_url)
req.add_data(urllib.urlencode(params))

print urllib.urlencode(params)

urllib.urlencode(params)
#req = urllib2.Request("%s?%s" % (frtl_url, urllib.urlencode(params)))
req.add_header("Authorization", "OAuth")
resp = urllib2.urlopen(req)

#import test
#tl = test.tw_xmlparse(resp.read())
#for post in tl.statuses:
#    print "@%s\t%s" % (post["user"]["screen_name"], post["text"])

print "Done!!"
