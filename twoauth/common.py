#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [common.py]
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
import time, datetime
import locale

def twittertime(timestr):
    # Sample
    # Wed Nov 18 18:54:12 +0000 2009
    format = "%m %d %H:%M:%S +0000 %Y"
    m = {
        'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 
        'Apr' : 4, 'May' : 5, 'Jun' : 6,
        'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 
        'Oct' : 10, 'Nov' : 11, 'Dec' : 12
        }
    
    t = "%02d %s" % (m[timestr[4:7]], timestr[8:])
    dt = datetime.datetime.strptime(t, format)
    offset = time.altzone if time.daylight else time.timezone
    dt -= datetime.timedelta(seconds = offset)
    return dt

def twittersource(source):
    if source == "web":
        return u"web"
    else:
        i = source.find(">")
        if i != -1:
            return unicode(source[i + 1:-4])
        else:
            return unicode(source)
