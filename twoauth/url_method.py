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

class TwitterURL(object):
    protocol_http = "http"
    protocol_https = "https"

    endpoint = "://api.twitter.com/1.1/"
    endpoint_upload = "://upload.twitter.com/1.1/"
    
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
            "update_with_media": "POST",
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
        "help" : {
            "configuration" : "GET",
            }
        }
    
    def __init__(self, is_ssl = True, response_type = "json"):
        if is_ssl:
            api = TwitterURL.protocol_https + TwitterURL.endpoint
        else:
            api = TwitterURL.protocol_http + TwitterURL.endpoint
        
        upload = TwitterURL.protocol_https + TwitterURL.endpoint_upload
        t = "." + response_type
        
        # Twitter REST API URLs
        self.url = {
            "statuses" : {
                "public_timeline" :
                    api + "statuses/public_timeline" + t,
                "home_timeline" :
                    api + "statuses/home_timeline" + t,
                "friends_timeline" :
                    api + "statuses/friends_timeline" + t,
                "user_timeline" :
                    api + "statuses/user_timeline" + t,
                "mentions" :
                    api + "statuses/mentions" + t,
                "retweeted_by_me" :
                    api + "statuses/retweeted_by_me" + t,
                "retweeted_to_me" :
                    api + "statuses/retweeted_to_me" + t,
                "retweets_of_me" :
                    api + "statuses/retweets_of_me" + t,
                "show" :
                    api + "statuses/show/${id}" + t,
                "update" :
                    api + "statuses/update" + t,
                "update_with_media":
                    upload + "statuses/update_with_media" + t,
                "destroy" :
                    api + "statuses/destroy/${id}" + t,
                "retweet" :
                    api + "statuses/retweet/${id}" + t,
                "retweets" :
                    api + "statuses/retweets/${id}" + t,
                "retweeted_by" :
                    api + "statuses/${id}/retweeted_by" + t,
                "retweeted_by_ids" :
                    api + "statuses/${id}/retweeted_by/ids" + t,
                "friends" :
                    api + "statuses/friends" + t,
                "followers" :
                    api + "statuses/followers" + t,
                },
            "users" : {
                "show" :
                    api + "users/show" + t,
                "lookup" :
                    api + "users/lookup" + t,
                "search" :
                    api + "users/search" + t,
                "profile_image" :
                    api + "users/profile_image/${user}" + t,
                "suggestions" :
                    api + "users/suggestions" + t,
                "suggestions_cat" :
                    api + "users/suggestions/${slug}" + t,
                },
            "account" : {
                "verify_credentials" :
                    api + "account/verify_credentials" + t,
                "rate_limit" :
                    api + "account/rate_limit_status" + t,
                "end_session" :
                    api + "account/end_session" + t,
                "delivery_device" :
                    api + "account/update_delivery_device" + t,
                "profile_colors" :
                    api + "account/update_profile_colors" + t,
                "profile_image" :
                    api + "account/update_profile_image" + t,
                "profile_back" :
                    api + "account/update_profile_background_image" + t,
                "update_profile" :
                    api + "account/update_profile" + t,
                },
            "lists" : {
                "create" :
                    api + "${user}/lists" + t,
                "update" :
                    api + "${user}/lists/${id}" + t,
                "index" :
                    api + "${user}/lists" + t,
                "show" :
                    api + "${user}/lists/${id}" + t,
                "destroy" :
                    api + "${user}/lists/${id}" + t,
                "statuses" :
                    api + "${user}/lists/${list_id}/statuses" + t,
                "memberships" :
                    api + "${user}/lists/memberships" + t,
                "subscriptions" :
                    api + "${user}/lists/subscriptions" + t,
                "mlist" :
                    api + "${user}/${list_id}/members" + t,
                "madd" :
                    api + "${user}/${list_id}/members" + t,
                "mremove" :
                    api + "${user}/${list_id}/members" + t,
                "mshow" :
                    api + "${user}/${list_id}/members/${id}" + t,
                "slist" :
                    api + "${user}/${list_id}/subscribers" + t,
                "sadd" :
                    api + "${user}/${list_id}/subscribers" + t,
                "sremove" :
                    api + "${user}/${list_id}/subscribers" + t,
                "sshow" :
                    api + "${user}/${list_id}/subscribers/${id}" + t,
                },
            "dm" : {
                "list" :
                    api + "direct_messages" + t,
                "sent" :
                    api + "direct_messages/sent" + t,
                "new" :
                    api + "direct_messages/new" + t,
                "destroy" :
                    api + "direct_messages/destroy/${id}" + t,
                },
            "friendship" : {
                "create" :
                    api + "friendships/create/${user}" + t,
                "destroy" :
                    api + "friendships/destroy/${user}" + t,
                "exists" :
                    api + "friendships/exists" + t,
                "show" :
                    api + "friendships/show" + t,
                "friends" :
                    api + "friends/ids" + t,
                "followers" :
                    api + "followers/ids" + t,
                "incoming" :
                    api + "friendships/incoming" + t,
                "outgoing" :
                    api + "friendships/outgoing" + t,
                },
            "favorite" : {
                "list" :
                    api + "favorites/${user}" + t,
                "create" :
                    api + "favorites/create/${id}" + t,
                "destroy" :
                    api + "favorites/destroy/${id}" + t,
                },
            "block" : {
                "create" :
                    api + "blocks/create" + t,
                "destroy"  :
                    api + "blocks/destroy" + t,
                "exists" :
                    api + "blocks/exists" + t,
                "blocking" :
                    api + "blocks/blocking" + t,
                "blockids" :
                    api + "blocks/blocking/ids" + t,
                "report_spam" :
                    api + "report_spam" + t,
                },
            "help" : {
                "configuration" :
                    api + "help/configuration" + t,
                }
            }
