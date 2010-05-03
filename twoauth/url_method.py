#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [url_method.py]
# - Hirotaka Kawata <info@techno-st.net>
# - http://www.techno-st.net/wiki/python-twoauth
#
#
# Copyright (c) 2009 Hirotaka Kawata
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

twurl = "http://api.twitter.com/1/"
#twurl = "http://twitter.com/"
apiurl = "http://api.twitter.com/1/"
t = ".xml"

# Twitter REST API URLs
url = {
    "statuses" : {
        "public_timeline" :
            twurl + "statuses/public_timeline" + t,
        "home_timeline" :
            apiurl + "statuses/home_timeline" + t,
        "friends_timeline" :
            twurl + "statuses/friends_timeline" + t,
        "user_timeline" :
            twurl + "statuses/user_timeline" + t,
        "mentions" :
            twurl + "statuses/mentions" + t,
        "retweeted_by_me" :
            apiurl + "statuses/retweeted_by_me" + t,
        "retweeted_to_me" :
            apiurl + "statuses/retweeted_to_me" + t,
        "retweets_of_me" :
            apiurl + "statuses/retweets_of_me" + t,
        "show" :
            twurl + "statuses/show/${id}" + t,
        "update" :
            twurl + "statuses/update" + t,
        "destroy" :
            twurl + "statuses/destroy/${id}" + t,
        "retweet" :
            apiurl + "statuses/retweet/${id}" + t,
        "retweets" :
            apiurl + "statuses/retweets/${id}" + t,
        "retweeted_by" :
            apiurl + "statuses/${id}/retweeted_by" + t,
        "retweeted_by_ids" :
            apiurl + "statuses/${id}/retweeted_by/ids" + t,
        "friends" :
            twurl + "statuses/friends" + t,
        "followers" :
            twurl + "statuses/followers" + t,
        },
    "users" : {
        "show" :
            twurl + "users/show" + t,
        "lookup" :
            twurl + "users/lookup" + t,
        "search" :
            apiurl + "users/search" + t,
        "suggestions" :
            apiurl + "users/suggestions" + t,
        "suggestions_cat" :
            apiurl + "users/suggestions/${slug}" + t,
        },
    "account" : {
        "verify_credentials" :
            twurl + "account/verify_credentials" + t,
        "rate_limit" :
            twurl + "account/rate_limit_status" + t,
        "end_session" :
            twurl + "account/end_session" + t,
        "delivery_device" :
            twurl + "account/update_delivery_device" + t,
        "profile_colors" :
            twurl + "account/update_profile_colors" + t,
        "profile_image" :
            twurl + "account/update_profile_image" + t,
        "profile_back" :
            twurl + "account/update_profile_background_image" + t,
        "update_profile" :
            twurl + "account/update_profile" + t,
        },
    "lists" : {
        "create" :
            apiurl + "${user}/lists" + t,
        "update" :
            apiurl + "${user}/lists/${id}" + t,
        "index" :
            apiurl + "${user}/lists" + t,
        "show" :
            apiurl + "${user}/lists/${id}" + t,
        "destroy" :
            apiurl + "${user}/lists/${id}" + t,
        "statuses" :
            apiurl + "${user}/lists/${list_id}/statuses" + t,
        "memberships" :
            apiurl + "${user}/lists/memberships" + t,
        "subscriptions" :
            apiurl + "${user}/lists/subscriptions" + t,
        "mlist" :
            apiurl + "${user}/${list_id}/members" + t,
        "madd" :
            apiurl + "${user}/${list_id}/members" + t,
        "mremove" :
            apiurl + "${user}/${list_id}/members" + t,
        "mshow" :
            apiurl + "${user}/${list_id}/members/${id}" + t,
        "slist" :
            apiurl + "${user}/${list_id}/subscribers" + t,
        "sadd" :
            apiurl + "${user}/${list_id}/subscribers" + t,
        "sremove" :
            apiurl + "${user}/${list_id}/subscribers" + t,
        "sshow" :
            apiurl + "${user}/${list_id}/subscribers/${id}" + t,
        },
    "dm" : {
        "list" :
            twurl + "direct_messages" + t,
        "sent" :
            twurl + "direct_messages/sent" + t,
        "new" :
            twurl + "direct_messages/new" + t,
        "destroy" :
            twurl + "direct_messages/destroy/${id}" + t,
        },
    "friendship" : {
        "create" :
            twurl + "friendships/create/${user}" + t,
        "destroy" :
            twurl + "friendships/destroy/${user}" + t,
        "exists" :
            twurl + "friendships/exists" + t,
        "show" :
            twurl + "friendships/show" + t,
        "friends" :
            twurl + "friends/ids" + t,
        "followers" :
            twurl + "followers/ids" + t,
        "incoming" :
            apiurl + "friendships/incoming" + t,
        "outgoing" :
            apiurl + "friendships/outgoing" + t,
        },
    "favorite" : {
        "list" :
            twurl + "favorites/${user}" + t,
        "create" :
            twurl + "favorites/create/${id}" + t,
        "destroy" :
            twurl + "favorites/destroy/${id}" + t,
        },
    "block" : {
        "create" :
            twurl + "blocks/create" + t,
        "destroy"  :
            twurl + "blocks/destroy" + t,
        "exists" :
            twurl + "blocks/exists" + t,
        "blocking" :
            twurl + "blocks/blocking" + t,
        "blockids" :
            twurl + "blocks/blocking/ids" + t,
        "report_spam" :
            apiurl + "report_spam" + t,
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
        "retweeted_by"     : "GET",
        "retweeted_by_ids" : "GET",
        "friends"          : "GET",
        "followers"        : "GET"
        },
    "users" : {
        "show"   : "GET",
        "search" : "GET",
        "lookup" : "GET",
        "suggestions"     : "GET",
        "suggestions_cat" : "GET",
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
        "incoming" : "GET",
        "outgoing" : "GET",
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
        "report_spam" : "POST",
        },
    }
