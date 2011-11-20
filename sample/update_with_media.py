#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import twoauth

if __name__ == "__main__":
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    text = sys.argv[5]
    filepath = sys.argv[6]
    
    api = twoauth.api(ckey, csecret, atoken, asecret)
    ret = api.status_update_with_media(text, filepath)
    
    print ret
