#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [status.py]
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

from common import twittersource, twittertime
import user

class twstatus(UserDict.UserDict):
    def __init__(self, d):
        status = dict(d)
        self.data = status
        
        if "delete" in status: return
        
        self.created_at = twittertime(status["created_at"])
        
        for i in ("id", "in_reply_to_status_id",
                  "in_reply_to_user_id"):
            setattr(self, i, int(status[i]) \
                        if status[i] != None else None)
        
        for i in ("text", "source", "in_reply_to_screen_name"):
            setattr(self, i, unicode(status[i]) \
                        if status[i] != None else None)
        
        self.source_name = twittersource(self.source)
        
        for i in ("favorited", "truncated"):
            setattr(self, i, status[i])
        
        if "user" in status.keys():
            self.user = user.twuser(status["user"])

        if "retweeted_status" in status.keys():
            self.retweeted_status = twstatus(status["retweeted_status"])
        else:
            self.retweeted_status = None
