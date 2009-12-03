#!/usr/bin/env python
#-*- coding: utf-8 -*-

import twoauth

if __name__ == "__main__":
    import sys
    
    api = twoauth.twoauth(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
    print "screen_name:", api.user["screen_name"]

    if False:
        print "Timeline:"
        tls = (api.public_timeline(),
               api.home_timeline(),
               api.friends_timeline(),
               api.user_timeline(),
               api.mentions(),
               api.rt_by_me(),
               api.rt_to_me(),
               api.rt_of_me())
        for tl in tls:
            for status in tl:
                print "%15s: %s" % (
                    status["user"]["screen_name"], status["text"])
            raw_input()

    if False:
        print "Status:"
        print api.status_show(6309158646)["text"]
        
        print "What are you doing?:",
        post = raw_input()
        postid = api.status_update(post)["id"]
        print postid
        raw_input()
        
        api.status_destroy(postid)
        print "Destroy!!"
        
        api.status_retweet(6305546787)
        print "ReTweet!!"
        
        for s in api.status_retweets(6305546787):
            print s["user"]["screen_name"]
        raw_input()

    if True:
        print "User:"
        print api.user_show(screen_name = "hktechno")["status"]["text"]

        tls = (api.user_search("python"),
               api.status_friends(),
               api.status_followers())
        
        for tl in tls:
            for s in tl:
                print s["screen_name"]
            raw_input()

    print "Lists:"
    for l in api.lists_memberships()["lists"]:
        print "%30s %s" % (l["full_name"], l["member_count"])

    print "ReTweet:"
    for status in api.rt_to_me(count = 10):
        print "Retweeted by %s: %s: %s" % (
            status["retweeted_status"]["user"]["screen_name"],
            status["user"]["screen_name"],
            status["retweeted_status"]["text"])
