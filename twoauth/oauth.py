#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [oauth.py]
# - Hirotaka Kawata <info@techno-st.net>
# - http://www.techno-st.net/wiki/python-twoauth
#
#
# Copyright (c) 2009-2010 Hirotaka Kawata
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
import string
import urllib, urllib2
import httplib
import urlparse
import hmac, hashlib
import cgi
import cStringIO

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

        random.seed()
    
    # Get Request Token
    def request_token(self):
        # initialize OAuth parameters
        oauth_params = self._init_params()
        del oauth_params["oauth_token"]
        
        # get OAuth header
        auth_header = self.oauth_header(self.reqt_url,
                                        oauth_params = oauth_params)
        
        # send request
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
        # set request token information
        token = token_info["oauth_token"]
        secret = token_info["oauth_token_secret"]
        
        # initialize OAuth parameters
        oauth_params = self._init_params(token)
        oauth_params["oauth_verifier"] = pin
        
        # get OAuth header
        auth_header = self.oauth_header(self.acct_url, secret = secret,
                                        oauth_params = oauth_params)
        
        # send request
        req = urllib2.Request(self.acct_url)
        req.add_header("Authorization", auth_header)
        resp = urllib2.urlopen(req)
        
        # Parse Access Token
        token_info = cgi.parse_qs(resp.read())
        for p in token_info:
            token_info[p] = token_info[p][0]
        
        # set token and secret to instance if not set
        if not self.atoken and not self.asecret:
            self.atoken = token_info["oauth_token"]
            self.asecret = token_info["oauth_token_secret"]
        
        return token_info
    
    # Return Authorization Header String
    def oauth_header(self, url, method = "GET", add_params = {}, secret = "", oauth_params = None):
        # initialize OAuth parameters if no given oauth_params
        if oauth_params == None:
            oauth_params = self._init_params()
        
        # get oauth_signature
        sig = self._make_signature(url, oauth_params, method, secret, add_params)
        oauth_params["oauth_signature"] = sig
        
        # quote OAuth format
        plist = []
        for p in oauth_params:
            plist.append('%s="%s"' % (
                    self._oquote(p), self._oquote(oauth_params[p])))
        
        return "OAuth %s" % (", ".join(plist))
    
    # Return urllib2.Request Object for OAuth
    def oauth_request(self, url, method = "GET", add_params = {}):
        # quote parameters
        enc_params = {}
        if add_params:
            api_params = urllib.urlencode(add_params)
            for p in add_params:
                enc_params[self._oquote(p)] = self._oquote(add_params[p])
        else:
            api_params = ""
        
        # create urllib2.Request
        if method == "GET":
            if add_params:
                req = urllib2.Request("%s?%s" % (url, api_params))
            else:
                req = urllib2.Request(url)
        elif method == "POST":
            req = urllib2.Request(url, api_params)
        else:
            raise
        
        # set OAuth header
        req.add_header("Authorization", 
                       self.oauth_header(url, method, enc_params, self.asecret))
        
        return req
    
    # Return httplib.HTTPResponse (for DELETE Method
    def oauth_http_request(self, url, method = "GET", add_params = {}, header = {}):
        enc_params = {}
        if add_params:
            api_params = urllib.urlencode(add_params)
            for p in add_params:
                enc_params[self._oquote(p)] = self._oquote(add_params[p])
        else:
            api_params = ""
        
        header["Authorization"] = self.oauth_header(url, method, enc_params, self.asecret)
        
        urlp = urlparse.urlparse(url)
        conn = httplib.HTTPConnection(urlp.netloc)
        
        if method == "GET":
            path = "%s?%s" % (urlp.path, api_params)
            conn.request(method, path, headers = header)
        else:
            conn.request(method, urlp.path, api_params, header)
        
        return conn
    
    # Get random string (for oauth_nonce)
    def _rand_str(self, n):
        seq = string.ascii_letters + string.digits
        return ''.join(random.choice(seq) for i in xrange(n))
    
    # Initialize OAuth parameters
    def _init_params(self, token = None):
        if token == None:
            token = self.atoken

        params = {
            "oauth_consumer_key": self.ckey,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_nonce": self._rand_str(10),
            "oauth_version": "1.0",
            "oauth_token" : token
            }
        
        return params
    
    # calculate oauth_signature
    def _make_signature(self, url, oauth_params, method = "GET", 
                        secret = "", add_params = {}):
        sigparams = {}
        sigparams.update(oauth_params)
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
    
    # quote string for OAuth format
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
