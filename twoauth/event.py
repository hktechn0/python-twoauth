#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [event.py]
# - Hirotaka Kawata <info@techno-st.net>
# - http://www.techno-st.net/wiki/python-twoauth
#
#
# Copyright (c) 2009-2011 Hirotaka Kawata
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
import status

class TwitterEvent(dict):
    def __init__(self, d):
        self.update(d)
        self["target"] = user.TwitterUser(d.get("target"))
        self["source"] = user.TwitterUser(d.get("source"))
        
        if "target_object" in d:
            self["target_object"] = status.TwitterStatus(d.get("target_object"))
    
    @property
    def target(self): return self["target"]
    
    @property
    def source(self): return self["source"]
    
    @property
    def target_object(self): return self.get("target_object")

    @property
    def created_at(self): return twittertime(self.get("created_at"))
    
    @property
    def event(self): return self.get("event")
    @property
    def type(self): return self.get("event")
