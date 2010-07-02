#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [twitpic.py]
# - Hirotaka Kawata <info@techno-st.net>
# - http://www.techno-st.net/wiki/python-twoauth
#
#
# Copyright (c) 2010 Hirotaka Kawata
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

# Twitpic API v2 wrapper methods

import httplib
import json
import email.mime.image
import email.mime.multipart
import email.mime.text
import email.encoders

import oauth

class Twitpic:
    host = "api.twitpic.com"
    url = "/2/upload.json"
    verify_credentials_url = "https://api.twitter.com/1/account/verify_credentials.json"
    
    def __init__(self, oauth, apikey):
        self.oauth = oauth
        self.apikey = apikey
    
    def upload(self, image, message = ""):
        imgdata = image.read()
        mimeimg = email.mime.image.MIMEImage(imgdata, _encoder = email.encoders.encode_noop)
        mimeimg.add_header("Content-Disposition", "form-data", name = "media", filename = "media")
        mimeimg.add_header("Content-Length", str(len(imgdata)))
        mimekey = email.mime.text.MIMEText(self.apikey)
        mimekey.add_header("Content-Disposition", "form-data", name = "key")
        mimemsg = email.mime.text.MIMEText(message)
        mimemsg.set_charset("utf-8")
        mimemsg.add_header("Content-Disposition", "form-data", name = "message")
        
        data = email.mime.multipart.MIMEMultipart("form-data")
        data.attach(mimekey)
        data.attach(mimemsg)
        data.attach(mimeimg)
        
        multipart = data.as_string()
        ctype, multipart = multipart.split("\n\n", 1)
        
        c = httplib.HTTPConnection(self.host)
        c.putrequest("POST", self.url)
        
        oauth_header = self.oauth.oauth_header(
            self.verify_credentials_url, 
            secret = self.oauth.asecret)
        oauth_header += ', realm="http://api.twitter.com/"'
        
        c.putheader("X-Verify-Credentials-Authorization",
                    oauth_header)
        c.putheader("X-Auth-Service-Provider",
                    self.verify_credentials_url)
        
        c.putheader("Content-Length", str(len(multipart)))
        c.putheader("Content-Type", ctype.split(": ", 1)[-1])
        
        c.endheaders()
        c.send(multipart)
        
        response = c.getresponse().read()
        return json.loads(response)

if __name__ == "__main__":
    import sys
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    filepath = sys.argv[5]
    
    # from python-twoauth
    apikey = "dcb62be3b2f310d4484f22364c1edd65"
    
    oauth = oauth.oauth(ckey, csecret, atoken, asecret)

    twpic = Twitpic(oauth, apikey)
    ret = twpic.upload(open(filepath, "rb"), "らりるれろ")

    print ret
