#!/usr/bin/env python
#-*- coding: utf-8 -*-

import twoauth

if __name__ == "__main__":
    import sys
    
    api = twoauth.api(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    timeline = False
    status = False
    user = False
    lists = False
    dm = False
    friendship = False
    account = False
    favorites = True
    
    print "screen_name:", api.user["screen_name"]

    if timeline:
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
            print len(tl)
            for status in tl:
                print "%15s: %s" % (
                    status["user"]["screen_name"], status["text"])
            raw_input()

    if status:
        print "Status:"
        print api.status_show(6309158646)["text"]
        
        print "What are you doing?:",
        post = raw_input()
        postid = api.status_update(post)["id"]
        print postid
        raw_input()
        
        api.status_destroy(postid)
        print "Destroy!!"
        
        try:
            api.status_retweet(6768575868)
        except Exception, e:
            print e.read()

        print "ReTweet!!"
        
        for s in api.status_retweets(6305546787):
            print s["user"]["screen_name"]
        raw_input()

    if user:
        print "User:"
        print api.user_show("hktechno")["status"]["text"]

        tls = (api.user_search("python"),
               api.status_friends(),
               api.status_followers())
        
        for tl in tls:
            for s in tl:
                print s["screen_name"]
            raw_input()

    if lists:
        print "Lists:"
        print "Create:",
        li = api.lists_create("testlist", mode = "private",
                              description = "testtest")
        lid = int(li["id"])
        print lid, li["full_name"]
        raw_input()

        print "Update:", 
        li = api.lists_update("testlist", name = "hogehoge", 
                              mode = "private", description = "hoge")
        print li["id"], li["full_name"]
        raw_input()

        print "Index:"
        for l in api.lists_index("hktechno")["lists"]:
            print l["full_name"]

        print "Show:",
        li = api.lists_show("team", "twitter")
        print li["full_name"], li["subscriber_count"], li["member_count"]

        print "Destroy:",
        print api.lists_destroy(lid)["id"]
        raw_input()
        
        print "Statuses:"
        for l in api.lists_statuses("team", "twitter", count = "10"):
            print "%20s %s" % (l["user"]["screen_name"], l["text"])
        
        print "Memberships:"
        for l in api.lists_memberships("hktechno")["lists"]:
            print "%30s %s" % (l["full_name"], l["member_count"])
        
        print "Subscriptions:"
        for l in api.lists_subscriptions("hktechno")["lists"]:
            print "%30s %s" % (l["full_name"], l["member_count"])
        raw_input()
            
    if dm:
        print "Direct Message"
        print "Inbox:"
        for dm in api.dm_list():
            print dm["text"]

        print "Sent:"
        for dm in api.dm_sent():
            print dm["text"]
        
        print "Send:"
        dm = api.dm_new("hktechno", "hello")
        raw_input()
        print "Destroy:"
        api.dm_destroy(dm["id"])
        raw_input()

    if friendship:
        print "Friendships:"

        print "Create:"
        api.friends_create("hktechno")

        print "Exists:"
        print api.friends_exists(api.user["id"], "hktechno")
        raw_input()

        print "Destroy:"
        api.friends_destroy("hktechno")

        print "Show:"
        print api.friends_show("hktechno")
        raw_input()

    if account:
        print "Account:"

        print "Verify Credentials:"
        a = api.verify_credentials()
        print a["id"]
        print a["name"]
        print a["screen_name"]
        print a["status"]["text"]

        print "Rate Limit:"
        print api.rate_limit(), api.rate_limit(True)

        print "End Session:"
        print api.end_session()
        raw_input()

        print "Update profile colors:"
        c = int(a["profile_background_color"])
        c = 0xffffff - c
        c = "%x" % c
        try:
            api.profile_colors(profile_background_color = c)
        except Exception, e:
            print e.read()

        print "Update profile:"
        import time
        api.profile(description = time.time())
        raw_input()

    if favorites:
        print "Favorites:"

        print "Create:"
        api.favorite_create(6861002055)

        print "Favorites:"
        for f in api.favorites():
            print "%s %s" % (f["user"]["screen_name"], f["text"])
        raw_input()

        print "Destroy:"
        api.favorite_destroy(6861002055)
        raw_input()
