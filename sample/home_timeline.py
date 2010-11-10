#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import twoauth

if __name__ == "__main__":
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    
    api = twoauth.api(ckey, csecret, atoken, asecret)
    
    # Get Home Timeline
    for status in api.home_timeline(count = 200):
        print status.user.screen_name, status.text
