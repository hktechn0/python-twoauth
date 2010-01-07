#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import twoauth

if __name__ == "__main__":
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    
    api = twoauth.api(
        ckey, csecret, atoken, asecret)
    
    friends = api.friends_ids()
    followers = api.followers_ids()
    
    fr = list()
    fo = list()

    for u in friends:
        fr.append(long(u))
    for u in followers:
        fo.append(long(u))
    
    for u in sorted(fr):
        if u in fo:
            fo.remove(u)
            print "<>", u
        else:
            print " >", u

    for u in sorted(fo):
        print "< ", u
