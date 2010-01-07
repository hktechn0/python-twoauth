#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# python-twoauth [url_method.py]
# - Hirotaka Kawata <info@techno-st.net>
# - http://www.techno-st.net/wiki/python-twoauth
#

twurl = "http://twitter.com/"
apiurl = "http://api.twitter.com/1/"
api_t = ".xml"

# Twitter REST API URLs
url = {
    "statuses" : {
        "public_timeline" :
            twurl + "statuses/public_timeline" + api_t,
        "home_timeline" :
            apiurl + "statuses/home_timeline" + api_t,
        "friends_timeline" :
            twurl + "statuses/friends_timeline" + api_t,
        "user_timeline" :
            twurl + "statuses/user_timeline" + api_t,
        "mentions" :
            twurl + "statuses/mentions" + api_t,
        "retweeted_by_me" :
            apiurl + "statuses/retweeted_by_me" + api_t,
        "retweeted_to_me" :
            apiurl + "statuses/retweeted_to_me" + api_t,
        "retweets_of_me" :
            apiurl + "statuses/retweets_of_me" + api_t,
        "show" :
            twurl + "statuses/show/" + "%id%" + api_t,
        "update" :
            twurl + "statuses/update" + api_t,
        "destroy" :
            twurl + "statuses/destroy/" + "%id%" + api_t,
        "retweet" :
            apiurl + "statuses/retweet/" + "%id%" + api_t,
        "retweets" :
            apiurl + "statuses/retweets/" + "%id%" + api_t,
        "friends" :
            twurl + "statuses/friends" + api_t,
        "followers" :
            twurl + "statuses/followers" + api_t
        },
    "users" : {
        "show" :
            twurl + "users/show" + api_t,
        "search" :
            apiurl + "users/search" + api_t
        },
    "account" : {
        "verify_credentials" :
            twurl + "account/verify_credentials" + api_t,
        "rate_limit" :
            twurl + "account/rate_limit_status" + api_t,
        "end_session" :
            twurl + "account/end_session" + api_t,
        "delivery_device" :
            twurl + "account/update_delivery_device" + api_t,
        "profile_colors" :
            twurl + "account/update_profile_colors" + api_t,
        "profile_image" :
            twurl + "account/update_profile_image" + api_t,
        "profile_back" :
            twurl + "account/update_profile_background_image" + api_t,
        "update_profile" :
            twurl + "account/update_profile" + api_t,
        },
    "lists" : {
        "create" :
            apiurl + "%user%/lists" + api_t,
        "update" :
            apiurl + "%user%/lists/%id%" + api_t,
        "index" :
            apiurl + "%user%/lists" + api_t,
        "show" :
            apiurl + "%user%/lists/%id%" + api_t,
        "destroy" :
            apiurl + "%user%/lists/%id%" + api_t,
        "statuses" :
            apiurl + "%user%/lists/%id%/statuses" + api_t,
        "memberships" :
            apiurl + "%user%/lists/memberships" + api_t,
        "subscriptions" :
            apiurl + "%user%/lists/subscriptions" + api_t,
        "mlist" :
            apiurl + "%user%/%list_id%/members" + api_t,
        "madd" :
            apiurl + "%user%/%list_id%/members" + api_t,
        "mremove" :
            apiurl + "%user%/%list_id%/members" + api_t,
        "mshow" :
            apiurl + "%user%/%list_id%/members/%id%" + api_t,
        "slist" :
            apiurl + "%user%/%list_id%/subscribers" + api_t,
        "sadd" :
            apiurl + "%user%/%list_id%/subscribers" + api_t,
        "sremove" :
            apiurl + "%user%/%list_id%/subscribers" + api_t,
        "sshow" :
            apiurl + "%user%/%list_id%/subscribers/%id%" + api_t,
        },
    "dm" : {
        "list" :
            twurl + "direct_messages" + api_t,
        "sent" :
            twurl + "direct_messages/sent" + api_t,
        "new" :
            twurl + "direct_messages/new" + api_t,
        "destroy" :
            twurl + "direct_messages/destroy/" + "%id%" + api_t,
        },
    "friendship" : {
        "create" :
            twurl + "friendships/create/%user%" + api_t,
        "destroy" :
            twurl + "friendships/destroy/%user%" + api_t,
        "exists" :
            twurl + "friendships/exists" + api_t,
        "show" :
            twurl + "friendships/show" + api_t,
        "friends" :
            twurl + "friends/ids" + api_t,
        "followers" :
            twurl + "followers/ids" + api_t,
        },
    "favorite" : {
        "list" :
            twurl + "favorites/%user%" + api_t,
        "create" :
            twurl + "favorites/create/%id%" + api_t,
        "destroy" :
            twurl + "favorites/destroy/%id%" + api_t,
        },
    "block" : {
        "create" :
            twurl + "blocks/create" + api_t,
        "destroy"  :
            twurl + "blocks/destroy" + api_t,
        "exists" :
            twurl + "blocks/exists" + api_t,
        "blocking" :
            twurl + "blocks/blocking" + api_t,
        "blockids" :
            twurl + "blocks/blocking/ids" + api_t,
        },
    }

# Twitter REST API Methods
method = {
    "statuses" : {
        "public_timeline"  : "GET",
        "home_timeline"    : "GET",
        "friends_timeline" : "GET",
        "user_timeline"    : "GET",
        "mentions"         : "GET",
        "retweeted_by_me"  : "GET",
        "retweeted_to_me"  : "GET",
        "retweets_of_me"   : "GET",
        "show"             : "GET",
        "update"           : "POST",
        "destroy"          : "POST",
        "retweet"          : "POST",
        "retweets"         : "GET",
        "friends"          : "GET",
        "followers"        : "GET"
        },
    "users" : {
        "show"   : "GET",
        "search" : "GET"
        },
    "account" : {
        "verify_credentials" : "GET",
        "rate_limit"         : "GET",
        "end_session"        : "POST",
        "delivery_device"    : "POST",
        "profile_colors"     : "POST",
        "profile_image"      : "POST",
        "profile_back"       : "POST",
        "update_profile"     : "POST",
        },
    "lists" : {
        "create"        : "POST",
        "update"        : "POST",
        "index"         : "GET",
        "show"          : "GET",
        "destroy"       : "DELETE",
        "statuses"      : "GET",
        "memberships"   : "GET",
        "subscriptions" : "GET",
        "mlist"         : "GET",
        "madd"          : "POST",
        "mremove"       : "DELETE",
        "mshow"         : "GET",
        "slist"         : "GET",
        "sadd"          : "POST",
        "sremove"       : "DELETE",
        "sshow"         : "GET",
        },
    "dm" : {
        "list"    : "GET",
        "sent"    : "GET",
        "new"     : "POST",
        "destroy" : "POST"
        },
    "friendship" : {
        "create"  : "POST",
        "destroy" : "POST",
        "exists"  : "GET",
        "show"    : "GET",
        "friends"   : "GET",
        "followers" : "GET",
        },
    "favorite" : {
        "list"    : "GET",
        "create"  : "POST",
        "destroy" : "POST",
        },
    "block" : {
        "create"   : "POST",
        "destroy"  : "POST",
        "exists"   : "GET",
        "blocking" : "GET",
        "blockids" : "GET",
        },
    }
