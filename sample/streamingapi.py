#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import twoauth
import twoauth.streaming

if __name__ == "__main__":
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    
    oauth = twoauth.oauth(ckey, csecret, atoken, asecret)
    
    s = twoauth.streaming.StreamingAPI(oauth)
    
    # User Streams start
    streaming = s.filter(track = ["twitter", u"ついったー", u"ツイッター"])
    streaming.start()
    
    while True:
        statuses = streaming.pop()
        for i in statuses:
            try:
                print i.user.screen_name, i.text
            except:
                print i
        
        streaming.event.wait()
