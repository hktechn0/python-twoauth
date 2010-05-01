#!/usr/bin/env python

import twoauth.oauth

url = raw_input("url:")
method = raw_input("method:")
ckey = raw_input("consumer_key:")
csecret = raw_input("consumer_secret:")
atoken = raw_input("access_token:")
asecret = raw_input("accsess_secret:")

oauth = twoauth.oauth(ckey, csecret, atoken, asecret)
oauth._init_params()
oauth.params["oauth_timestamp"] = raw_input("timestamp:")
oauth.params["oauth_nonce"] = raw_input("nonce:")
params = dict(eval(raw_input("add_params (python dict):\n")))
signature = oauth._make_signature(url, method, asecret, params)

print signature
