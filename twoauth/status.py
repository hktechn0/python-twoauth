#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [status.py]
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

from common import twittersource, twittertime
import user

class TwitterStatus(dict):
    def __init__(self, d):
        self.update(d)        
        self["user"] = user.TwitterUser(self.get("user"))

    @property
    def favorited(self): return bool(self.get("favorited"))
    @favorited.setter
    def favorited(self, value): self["favorited"] = bool(value)
    
    @property
    def created_at(self): return twittertime(self.get("created_at"))
    
    @property
    def text(self): return self.get("text")
    @property
    def id(self): return self.get("id")
    
    @property
    def in_reply_to_user_id(self): return self.get("in_reply_to_user_id")
    @property
    def in_reply_to_screen_name(self): return self.get("in_reply_to_screen_name")
    
    @property
    def source(self): return self.get("source")
    @property
    def source_name(self): return twittersource(self.get("source"))
    @property
    def in_reply_to_status_id(self): return self.get("in_reply_to_status_id")
    
    @property
    def retweeted_status(self):
        rtstatus = self.get("retweeted_status")
        return TwitterStatus(rtstatus) if rtstatus != None else None
    
    @property
    def user(self): return self.get("user")
