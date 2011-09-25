#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [user.py]
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

from common import twittertime
import status

class TwitterUser(dict):
    def __init__(self, d):
        self.update(d)
    
    @property
    def id(self): return self.get("id")
    @property
    def followers_count(self): return self.get("followers_count")
    @property
    def friends_count(self): return self.get("friends_count")
    @property
    def favourites_count(self): return self.get("favourites_count")
    @property
    def statuses_count(self): return self.get("statuses_count")
    
    @property
    def protected(self): return self.get("protected")
    
    @property
    def following(self): return self.get("following")
    @following.setter
    def following(self, value): self["following"] = bool(value)
    
    @property
    def verified(self): return self.get("verified")
    
    @property
    def name(self): return self.get("name")
    @property
    def screen_name(self): return self.get("screen_name")
    @property
    def location(self): return self.get("location")
    @property
    def description(self): return self.get("description")
    
    @property
    def profile_image_url(self): return self.get("profile_image_url")
    @property
    def url(self): return self.get("url")
    @property
    def time_zone(self): return self.get("time_zone")
    
    @property
    def created_at(self): return twittertime(self.get("created_at"))
        
    @property
    def status(self): return status.TwitterStatus(self.get("status")) if self.get("status") != None else None
