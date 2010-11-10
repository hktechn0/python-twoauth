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

class oauth(object):
    _randchars = string.ascii_letters + string.digits
    
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
        for p in token_info.keys():
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
        for p in token_info.keys():
            token_info[p] = token_info[p][0]
        
        # set token and secret to instance if not set
        if not self.atoken and not self.asecret:
            self.atoken = token_info["oauth_token"]
            self.asecret = token_info["oauth_token_secret"]
        
        return token_info
    
    # calculate oauth_signature
    def oauth_signature(self, url, method = "GET", secret = "", *params):
        sigparams = {}
        for d in params: sigparams.update(d)
        
        # Generate Signature Base String
        plist = ["%s=%s" % (k, v) for k, v in sorted(sigparams.items())]
        
        pstr = "&".join(plist)
        msg = "%s&%s&%s" % (method, self._oquote(url), self._oquote(pstr))
        
        # Calculate Signature
        h = hmac.new("%s&%s" % (self.csecret, secret), msg, hashlib.sha1)
        sig = h.digest().encode("base64").strip()
        
        return sig
    
    # Return Authorization Header String
    def oauth_header(self, url, method = "GET", params = {}, secret = "", oauth_params = None):
        # initialize OAuth parameters if no given oauth_params
        if oauth_params == None:
            oauth_params = self._init_params()
        
        # Encode params for OAuth format
        keys = map(self._oquote, params.iterkeys())
        values = map(self._oquote, params.itervalues())
        enc_params = dict(zip(keys, values))
        
        # get oauth_signature
        sig = self.oauth_signature(url, method, secret, oauth_params, enc_params)
        oauth_params["oauth_signature"] = sig
        
        # quote OAuth format
        plist = ['%s="%s"' % (self._oquote(k), self._oquote(v)) for k, v in oauth_params.iteritems()]
        
        return "OAuth %s" % (", ".join(plist))
    
    # Return urllib2.Request Object for OAuth
    def oauth_request(self, url, method = "GET", params = {}):
        # create urllib2.Request
        if method == "GET":
            if params:
                req = urllib2.Request("%s?%s" % (url, urllib.urlencode(params)))
            else:
                req = urllib2.Request(url)
        elif method == "POST":
            req = urllib2.Request(url, urllib.urlencode(params))
        else:
            raise
        
        # set OAuth header
        req.add_header("Authorization", 
                       self.oauth_header(url, method, params, self.asecret))
        
        return req
    
    # Return httplib.HTTPResponse (for DELETE Method
    def oauth_http_request(self, url, method = "GET", params = {}, header = {}):        
        urlp = urlparse.urlparse(url)
        conn = httplib.HTTPConnection(urlp.netloc)
        
        header["Authorization"] = self.oauth_header(url, method, params, self.asecret)
        
        if method == "GET":
            path = "%s?%s" % (urlp.path, urllib.urlencode(params))
            conn.request(method, path, headers = header)
        else:
            conn.request(method, urlp.path, urllib.urlencode(params), header)
        
        return conn
    
    # Get random string (for oauth_nonce)
    def _rand_str(self, n):
        return ''.join(random.choice(self._randchars) for i in xrange(n))
    
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
    
    # quote string for OAuth format
    def _oquote(self, s):
        return urllib.quote(str(s), "-._~")
