#!/usr/bin/env python
#-*- coding: utf-8 -*-

import twoauth

# Input Consumer key, secret
ckey = raw_input("Consumer key: ")
csecret = raw_input("Consumer secret: ")

# Get Request Token and PIN URL
oauth = twoauth.oauth(ckey, csecret)
req_token = oauth.request_token()
url = oauth.authorize_url(req_token)

print "Authorize URL:", url
pin = raw_input("PIN: ")

# Get Access token
acc_token = oauth.access_token(req_token, pin)

print "screen_name: %s" % acc_token["screen_name"]
print "Access token: %s" % acc_token["oauth_token"]
print "Access token secret: %s" % acc_token["oauth_token_secret"]
