#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [twitterxml.py]
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

# XML Parser for Twitter API

import urllib2
import xml.parsers.expat
import UserDict
from status import twstatus
from user import twuser

class twitterxml:
    def __init__(self, xmlstr):
        # stack
        self.name = list()
        self.data = list()
        self.cdata = unicode()

        # mode stack
        self.mode = list()
        self.nmode = str()
        
        # XML Parser
        self.p = xml.parsers.expat.ParserCreate()
        self.p.StartElementHandler = self.start_element
        self.p.CharacterDataHandler = self.char_data
        self.p.EndElementHandler = self.end_element
        self.p.Parse(xmlstr)
    
    def start_element(self, name, attrs):
        # push element name
        self.name.append(name)
        self.mode.append(self.nmode)
        self.cdata = unicode()
        self.nmode = str()
        
        # type="array" mode check
        if "type" in attrs.keys():
            if attrs["type"] == "array":
                self.nmode = "array"
        
        if name == "ids":
            self.nmode = "array"
    
    def end_element(self, name):
        # character data strip
        d = self.cdata.strip(" \n")
        self.cdata = unicode()

        # pop mode and set next mode
        mode = self.mode.pop()
        self.nmode = mode
        
        if d:
            #d = int(d) \
            #    if d.isdigit() and name[-2:] == "id" else d
            if d == "true": d = True
            elif d == "false": d = False
            
            if mode:
                # for ids
                self.data.append(d)
            else:
                # string element
                self.data.append([name, d])
        elif self.name and name == self.name[-1]:
            # empty element
            self.data.append([name, None])
        else:
            elements = []
            while self.name.pop() != name:
                elements.append(self.data.pop())
            
            self.name.append(name)

            if mode:
                if name == "status":
                    self.data.append(twstatus(elements))
                elif name == "user":
                    self.data.append(twuser(elements))
                else:
                    # array element
                    self.data.append(dict(elements))
            else:
                if isinstance(elements[0], (dict, twstatus, twuser)):
                    # array parent
                    self.data.append((name, elements))
                else:
                    # others
                    if name == "status":
                        self.data.append((name, twstatus(elements)))
                    elif name == "user":
                        self.data.append((name, twuser(elements)))
                    elif name == "ids":
                        # for ids
                        self.data.append((name, tuple(elements)))
                    else:
                        self.data.append((name, dict(elements)))
    
    def char_data(self, c):
        self.cdata += c

def xmlparse(xml_text):
    parsed = twitterxml(xml_text)
    parsed.data = parsed.data[0][1]
    
    return parsed.data

if __name__ == '__main__':
    #url = 'http://twitter.com/statuses/public_timeline.xml'
    url = 'http://twitter.com/statuses/user_timeline.xml?screen_name=hktechno'
    xml_tl = urllib2.urlopen(url).read()

    tl = xmlparse(xml_tl)

    for post in tl:
        print "@%s\t%s" % (post["user"]["screen_name"], post["text"])
