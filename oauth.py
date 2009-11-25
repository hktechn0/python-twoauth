import time, random
import urllib, urllib2
import hmac, hashlib
import cgi

#
# Twitter OAuth Sample Script
# * techno - Hirotaka Kawata
# * http://techno-st.net/
#

# Consumer Key
ckey = "7DQXjee115WTfglhYAAVeA"
# Consumer Secret
csecret = "vwrnw41FBaWaIqB2eRk11rbH2wdtkIS76AVf8eZ4"

# Access Token
atoken = ""
# Access Token Secret
atoken_secret = ""

def make_signature(params, url, method, csecret, secret = ""):
    # Generate Signature Base String
    plist = []
    for i in sorted(params):
        plist.append("%s=%s" % (i, params[i]))

    pstr = "&".join(plist)
    msg = "%s&%s&%s" % (method, urllib.quote(url, ""), 
                        urllib.quote(pstr, ""))

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

def oauth_header(params):
    plist = []
    for p in params:
        plist.append('%s="%s"' % (p, urllib.quote(params[p])))
        
    return "OAuth %s" % (", ".join(plist))

# Request Token URL
reqt_url = 'http://twitter.com/oauth/request_token'
# Authorize URL
auth_url = 'http://twitter.com/oauth/authorize'
# Access Token URL
acct_url = 'http://twitter.com/oauth/access_token'
# status update
post_url = 'http://twitter.com/statuses/update.xml'
# show friends timeline
frtl_url = 'http://twitter.com/statuses/friends_timeline.xml'

if not atoken and not atoken_secret:
    # Request Parameters
    params = init_params()

    print "Get request token:",
    
    # Generate Signature
    sig = make_signature(params, reqt_url, "GET", csecret)
    params["oauth_signature"] = sig

    # Get Token
    req = urllib2.Request("%s?%s" % (reqt_url, urllib.urlencode(params)))
    resp = urllib2.urlopen(req)
    
    print "\t[OK]"
    
    # Parse Token Parameters
    ret = cgi.parse_qs(resp.read())
    token = ret["oauth_token"][0]
    token_secret = ret["oauth_token_secret"][0]

    # Get PIN
    print "* Please access to this URL, and allow."
    print "> %s?%s=%s" % (auth_url, "oauth_token", token)
    print "\n* After that, will display 7 digit PIN, input here."
    print "PIN ->",
    pin = raw_input()
    pin = int(pin)
    
    print "Get access token:",
    
    # Generate Access Token Request
    params = init_params()
    params["oauth_verifier"] = pin
    params["oauth_token"] = token
    
    sig = make_signature(params, acct_url, "GET", csecret, token_secret)
    params["oauth_signature"] = sig
    
    # Get Access Token
    req = urllib2.Request("%s?%s" % (acct_url, urllib.urlencode(params)))
    resp = urllib2.urlopen(req)
    
    print "\t[OK]"
    
    # Parse Access Token
    fin = cgi.parse_qs(resp.read())
    atoken = fin["oauth_token"][0]
    atoken_secret = fin["oauth_token_secret"][0]
    
    print "Access Token: %s" % atoken
    print "Access Token Secret: %s" % atoken_secret
    
    print "Your screen_name is '%s'." % fin["screen_name"][0]
    

# Update Status by OAuth Authorization
print "What are you doing?:",
post = raw_input()

params = init_params()
params["oauth_token"] = atoken
params["status"] = urllib.quote(post, "")

sig = make_signature(params, post_url, "POST", csecret, atoken_secret)
params["oauth_signature"] = sig

del params["status"]

req = urllib2.Request(post_url)
req.add_data("status=%s" % urllib.quote(post, ""))
req.add_header("Authorization", oauth_header(params))

try:
    resp = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print "Error: %s" % e
    print e.read()

# Get Friends Timeline by OAuth Authorization
params = init_params()
params["oauth_token"] = atoken

sig = make_signature(params, frtl_url, "GET", csecret, atoken_secret)
params["oauth_signature"] = sig

req = urllib2.Request(frtl_url)
req.add_header("Authorization", oauth_header(params))
resp = urllib2.urlopen(req)

# Show Timeline
import xml_parse
tl = xml_parse.tw_xmlparse(resp.read())
for post in tl.statuses:
    print "%10s: %s" % (post["user"]["screen_name"], post["text"])

print "Done!!"
