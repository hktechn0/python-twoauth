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
    
    while True:
        dml = api.dm_list()
        if not dml:
            break

        for dm in dml:
            print dm["id"]
            api.dm_destroy(dm["id"])
