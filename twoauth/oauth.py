#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [oauth.py]
# - Hirotaka Kawata <info@techno-st.net>
# - http://www.techno-st.net/wiki/python-twoauth
#
#
# Copyright (c) 2009 Hirotaka Kawata
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

# OAuth Module for Twitter

import time
import random
import urllib, urllib2
import httplib
import urlparse
import hmac, hashlib
import cgi

class oauth():
    def __init__(self, ckey, csecret, atoken = "", asecret = "",
                 site = "http://twitter.com/"):
        # Request Token URL
        self.reqt_url = site + 'oauth/request_token'
        # Authorize URL
        self.auth_url = site + 'oauth/authorize'
        # Access Token URL
        self.acct_url = site + 'oauth/access_token'

        # Consumer Key, Secret
        self.ckey = ckey
        self.csecret = csecret

        # Access Key, Secret
        self.atoken = atoken
        self.asecret = asecret
    
    # Get Request Token
    def request_token(self):
        self._init_params()
        del self.params["oauth_token"]
        
        auth_header = self.oauth_header(self.reqt_url)

        req = urllib2.Request(self.reqt_url)
        req.add_header("Authorization", auth_header)
        resp = urllib2.urlopen(req)
        
        # Parse Token Parameters
        token_info = cgi.parse_qs(resp.read())
        for p in token_info:
            token_info[p] = token_info[p][0]
        
        return token_info
    
    # Get Authorize URL
    def authorize_url(self, token_info):
        return "%s?%s=%s" % (
            self.auth_url, "oauth_token", token_info["oauth_token"])
    
    # Get Access Token
    def access_token(self, token_info, pin):
        token = token_info["oauth_token"]
        secret = token_info["oauth_token_secret"]

        self._init_params(token)
        self.params["oauth_verifier"] = pin

        auth_header = self.oauth_header(self.acct_url, secret = secret)
        
        req = urllib2.Request(self.acct_url)
        req.add_header("Authorization", auth_header)
        resp = urllib2.urlopen(req)
        
        # Parse Access Token
        token_info = cgi.parse_qs(resp.read())
        for p in token_info:
            token_info[p] = token_info[p][0]
        
        if not self.atoken and not self.asecret:
            self.atoken = token_info["oauth_token"]
            self.asecret = token_info["oauth_token_secret"]
        
        return token_info
    
    # Return Authorization Header String
    def oauth_header(self, url, method = "GET", add_params = {}, secret = ""):
        sig = self._make_signature(url, method, secret, add_params)
        self.params["oauth_signature"] = sig
        
        plist = []
        for p in self.params:
            plist.append('%s="%s"' % (
                    self._oquote(p), self._oquote(self.params[p])))
        
        return "OAuth %s" % (", ".join(plist))
    
    # Return urllib2.Request Object for OAuth
    def oauth_request(self, url, method = "GET", add_params = {}):
        self._init_params()

        enc_params = {}
        if add_params:
            api_params = urllib.urlencode(add_params)
            for p in add_params:
                enc_params[self._oquote(p)] = self._oquote(add_params[p])
        else:
            api_params = ""
        
        if method == "GET":
            if add_params:
                req = urllib2.Request("%s?%s" % (url, api_params))
            else:
                req = urllib2.Request(url)
        elif method == "POST":
            req = urllib2.Request(url, api_params)
        else:
            raise
        
        req.add_header("Authorization", self.oauth_header(
                url, method, enc_params, secret = self.asecret))
        
        return req

    # Return httplib.HTTPResponse (for DELETE Method
    def oauth_http_request(self, url, method = "GET", add_params = {}):
        self._init_params()
        
        enc_params = {}
        if add_params:
            api_params = urllib.urlencode(add_params)
            for p in add_params:
                enc_params[self._oquote(p)] = self._oquote(add_params[p])
        else:
            api_params = ""
        
        urlp = urlparse.urlparse(url)
        con = httplib.HTTPConnection(urlp.netloc)
        
        con.request(method, urlp.path, api_params, {
                "Authorization" : 
                self.oauth_header(url, method, enc_params, self.asecret)})
        
        return con.getresponse()
    
    def _init_params(self, token = None):
        if token == None:
            token = self.atoken

        self.params = {
            "oauth_consumer_key": self.ckey,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_nonce": str(random.getrandbits(64)),
            "oauth_version": "1.0",
            "oauth_token" : token
            }
    
    def _make_signature(self, url, method = "GET", 
                        secret = "", add_params = {}):
        sigparams = {}
        sigparams.update(self.params)
        sigparams.update(add_params)
        
        # Generate Signature Base String
        plist = []
        for i in sorted(sigparams):
            plist.append("%s=%s" % (i, sigparams[i]))
        
        pstr = "&".join(plist)
        msg = "%s&%s&%s" % (
            method, self._oquote(url), self._oquote(pstr))
        
        # Calculate Signature
        h = hmac.new("%s&%s" % (
                self.csecret, secret), msg, hashlib.sha1)
        sig = h.digest().encode("base64").strip()
        
        return sig
    
    def _oquote(self, s):
        return urllib.quote(str(s), "-._~")

if __name__ == "__main__":
    import sys
    ckey = sys.argv[1]
    csecret = sys.argv[2]

    oa = oauth(ckey, csecret)
    req_token = oa.request_token()
    auth_url = oa.authorize_url(req_token)

    print "Authorize URL:"
    print auth_url
    print "PIN:",
    pin = raw_input()

    acc_token = oa.access_token(req_token, pin)

    print "Screen Name: %s" % acc_token["screen_name"]
    print "Access Token: %s" % acc_token["oauth_token"]
    print "Access Token Secret: %s" % acc_token["oauth_token_secret"]
    
    # status update
    post_url = 'http://twitter.com/statuses/update.xml'
    # show friends timeline
    frtl_url = 'http://twitter.com/statuses/friends_timeline.xml'

    # Update Status by OAuth Authorization
    print "What are you doing?:",
    post = raw_input()
    
    req = oa.oauth_request(post_url, "POST", {"status" : post})
    
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print "Error: %s" % e
        print e.read()
    
    # Get Friends Timeline by OAuth Authorization
    req = oa.oauth_request(frtl_url)
    resp = urllib2.urlopen(req)
    print resp.read(500)
