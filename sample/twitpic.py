#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import twoauth
import twoauth.twitpic

if __name__ == "__main__":
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    filepath = sys.argv[5]
    
    # from python-twoauth
    apikey = "dcb62be3b2f310d4484f22364c1edd65"
    
    oauth = twoauth.oauth(ckey, csecret, atoken, asecret)

    twpic = twoauth.twitpic.Twitpic(oauth, apikey)
    ret = twpic.upload(open(filepath, "rb"), "らりるれろ")
    
    print ret
