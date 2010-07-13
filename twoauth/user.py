#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [user.py]
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

import UserDict

from common import twittertime
import status

class twuser(UserDict.UserDict):
    def __init__(self, d):
        user = dict(d)
        self.data = user
        
        for i in ("id", 
                  "followers_count", "friends_count", 
                  "favourites_count", 
                  "utc_offset", "statuses_count"):
            setattr(self, i, int(user[i]) if user[i] != None else None)
        
        for i in ("protected", "following", "verified"):
            setattr(self, i,  user[i])
        
        for i in ("name", "screen_name", "location",
                  "description", "profile_image_url",
                  "url", "time_zone"):
            setattr(self, i, unicode(user[i]) if user[i] != None else None)
        
        self.created_at = twittertime(user["created_at"])
        
        if "status" in user.keys():
            self.status = status.twstatus(user["status"])
