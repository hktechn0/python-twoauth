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
    
    friends = list()
    followers = list()

    print "Getting friends..."
    cursor = -1    
    while cursor != 0:
        print cursor
        a = api.friends(cursor = cursor)
        cursor = long(a["next_cursor"])
        friends.extend(a["users"])
    
    print "Getting followers..."
    cursor = -1
    while cursor != 0:
        print cursor
        a = api.followers(cursor = cursor)
        cursor = long(a["next_cursor"])
        followers.extend(a["users"])

    print "Getting friend_ids"
    friend_ids = api.friends_ids()
    print "Getting follower_ids"
    follower_ids = api.followers_ids()

    fr = list()
    fo = list()

    for u in friend_ids:
        fr.append(long(u))
    for u in follower_ids:
        fo.append(long(u))

    fr = sorted(fr)
    fo = sorted(fo)
    
    both = list()
    ing = list()
    by = list()

    for u in friends:
        uid = long(u["id"])
        if uid in fo:
            # Following AND Followed_by
            both.append((uid, u["screen_name"], True, True))
        else:
            # Following only
            ing.append((uid, u["screen_name"], True, False))

    for u in followers:
        uid = long(u["id"])
        if uid not in fr:
            # Followed_by only
            by.append((uid, u["screen_name"], False, True))

    l = sorted(both)
    l.extend(sorted(ing))
    l.extend(sorted(by))

    for i in l:
        print "<" if i[3] else " ", ">" if i[2] else " ", i[0], i[1]
