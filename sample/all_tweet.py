#!/usr/bin/env python

import sys
import twoauth

if __name__ == "__main__":
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    
    api = twoauth.api(
        ckey, csecret, atoken, asecret)

    maxid = ""
    tl = True
    
    while tl:
        try:
            tl = api.user_timeline(auth = True, max_id = maxid, count = 200)
        except:
            continue

        for s in tl[::-1]:
            print s["id"], s["text"].encode("utf-8"), s["created_at"]

        maxid = int(tl[0]["id"]) - 1
