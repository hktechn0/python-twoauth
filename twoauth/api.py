#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# python-twoauth [api.py]
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

# Twitter REST API wrapper methods

import sys
import urllib, urllib2
import string
import datetime
import oauth
import twitterxml

class api():
    # url, method
    from url_method import url, method
    
    def __init__(self, ckey, csecret, atoken, asecret,
                 screen_name = "", oauth_obj = None):
        # Oauth init
        if oauth_obj == None:
            self.oauth = oauth.oauth(ckey, csecret, atoken, asecret)
        else:
            self.oauth = oauth_obj
        
        self.user = { "screen_name" : screen_name }
        
        # ratelimit var init
        self.ratelimit_limit = -1
        self.ratelimit_remaining = -1
        self.ratelimit_reset = datetime.datetime.now()

        self.ratelimit_iplimit = -1
        self.ratelimit_ipremaining = -1
        self.ratelimit_ipreset = datetime.datetime.now()
    
    # Option initialization method
    # Only for backward compatibility...    
    def initialize(self):
        # Get user info
        req = self.oauth.oauth_request(
            self.url["account"]["verify_credentials"])
        xml = urllib2.urlopen(req).read()
        self.user = twitterxml.xmlparse(xml)
        
        # Get rate limit
        limit = self.rate_limit()
        self.ratelimit_limit = int(limit["hourly-limit"])
        self.ratelimit_remaining = int(limit["remaining-hits"])
        self.ratelimit_reset = datetime.datetime.fromtimestamp(
            int(limit["reset-time-in-seconds"]))

        iplimit = self.rate_limit(ip_limit = True)
        self.ratelimit_iplimit = int(iplimit["hourly-limit"])
        self.ratelimit_ipremaining = int(iplimit["remaining-hits"])
        self.ratelimit_ipreset = datetime.datetime.fromtimestamp(
            int(iplimit["reset-time-in-seconds"]))
    
    def _api(self, a, b, params = {}, noauth = False, **replace):
        url = self._urlreplace(a, b, replace)
        method = self.method[a][b]
        params = self._rm_noparams(params)
        params = self._convert_str_params(params)
        
        if noauth:
            # try no auth request
            try:
                return self._api_noauth(url, params)
            except urllib2.HTTPError, e:
                if e.code in (401, 403): pass
                else:                    raise
        
        req = self.oauth.oauth_request(url, method, params)
        data = urllib2.urlopen(req)
        
        header = data.info()
        self._set_ratelimit(header)
        
        xml = data.read()
        return twitterxml.xmlparse(xml)
    
    def _api_noauth(self, url, params):
        # No use OAuth, GET only
        paramstr = urllib.urlencode(params)
        
        data = urllib2.urlopen("%s?%s" % (url, paramstr))
        
        header = data.info()
        self._set_ratelimit_ip(header)
        
        xml = data.read()
        return twitterxml.xmlparse(xml)
    
    def _api_delete(self, a, b, params = {}, **replace):
        url = self._urlreplace(a, b, replace)
        
        params = self._rm_noparams(params)
        params = self._convert_str_params(params)
        
        conn = self.oauth.oauth_http_request(url, "DELETE", params)
        response = conn.getresponse()
        
        return twitterxml.xmlparse(response.read())
    
    def _set_ratelimit(self, header):
        try:
            self.ratelimit_limit = int(header["X-RateLimit-Limit"])
            self.ratelimit_remaining = int(header["X-RateLimit-Remaining"])
            self.ratelimit_reset = datetime.datetime.fromtimestamp(
                int(header["X-RateLimit-Reset"]))
        except KeyError:
            pass

    def _set_ratelimit_ip(self, header):
        try:
            self.ratelimit_iplimit = int(header["X-RateLimit-Limit"])
            self.ratelimit_ipremaining = int(header["X-RateLimit-Remaining"])
            self.ratelimit_ipreset = datetime.datetime.fromtimestamp(
                int(header["X-RateLimit-Reset"]))
        except KeyError:
            pass
    
    def _rm_noparams(self, params):
        flg = True
        while flg:
            flg = False
            for p in params:
                if not params[p]:
                    del params[p]
                    flg = True
                    break
        return params

    def _convert_str_params(self, params):
        for i in params:
            if isinstance(params[i], unicode):
                params[i] = str(params[i].encode("utf-8"))

        return params
    
    def _idtype(self, uid, ret = ("user_id", "screen_name"), 
                is_screen_name = False):
        if str(uid).isdigit() and not is_screen_name:
            # numeric id
            return ret[0]
        else:
            # screen_name
            return ret[1]

    def _urlreplace(self, a, b, replace):
        url = self.url[a][b]
        
        # if user not in replace list, add auth user
        if "user" not in replace or not replace["user"]:
            if "screen_name" in self.user:
                replace["user"] = self.user["screen_name"]
        
        tmpl = string.Template(url)
        rurl = tmpl.substitute(replace)
        
        return rurl
    
    #
    # Timeline Methods
    #
    def public_timeline(self, auth = False, **params):
        return self._api("statuses", "public_timeline", noauth = not auth)
    
    def home_timeline(self, **params):
        return self._api("statuses", "home_timeline", params)
    
    def friends_timeline(self, **params):
        return self._api("statuses", "friends_timeline", params)
    
    def user_timeline(self, user = "", is_screen_name = False,
                      auth = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        data = self._api("statuses", "user_timeline", params, noauth = not auth)
        return data
    
    def mentions(self, **params):
        return self._api("statuses", "mentions", params)
    
    def rt_by_me(self, **params):
        print >>sys.stderr, "[warning] Deprecated method: rt_by_me => retweeted_by_me"
        self.retweeted_by_me(**params)
    def retweeted_by_me(self, **params):
        return self._api("statuses", "retweeted_by_me", params)
    
    def rt_to_me(self, **params):
        print >>sys.stderr, "[warning] Deprecated method: rt_to_me => retweeted_to_me"
        self.retweeted_to_me(**params)
    def retweeted_to_me(self, **params):
        return self._api("statuses", "retweeted_to_me", params)
    
    def rt_of_me(self, **params):
        print >>sys.stderr, "[warning] Deprecated method: rt_of_me => retweets_of_me"
        self.retweets_of_me(**params)
    def retweets_of_me(self, **params):
        return self._api("statuses", "retweets_of_me", params)
    
    #
    # Status Methods
    #
    def status_show(self, _id, auth = False, **params):
        return self._api("statuses", "show", noauth = not auth, id = long(_id))
    
    def status_update(self, status, **params):
        params["status"] = status
        return self._api("statuses", "update", params)
    
    def status_destroy(self, _id, **params):
        return self._api("statuses", "destroy", params, id = long(_id))
    
    def status_retweet(self, _id, **params):
        return self._api("statuses", "retweet", params, id = long(_id))
    
    def status_retweets(self, _id, **params):
        return self._api("statuses", "retweets", params, id = long(_id))

    def status_retweeted_by(self, _id, **params):
        return self._api("statuses", "retweeted_by", params, id = long(_id))

    def status_retweeted_by_ids(self, _id, **params):
        return self._api("statuses", "retweeted_by_ids", params, id = long(_id))
    
    #
    # User Methods
    #
    def user_show(self, user, is_screen_name = False, auth = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("users", "show", params, noauth = not auth)

    def user_lookup(self, user_id = [], screen_name = [], **params):
        params["user_id"] = ",".join(user_id)
        params["screen_name"] = ",".join(user_id)
        return self._api("users", "lookup", params)
    
    def user_search(self, q, **params):
        params["q"] = q
        return self._api("users", "search", params)
    
    def users_suggestions(self, **params):
        return self._api("users", "suggestions", params)

    def users_suggestions_category(self, category, **params):
        return self._api("users", "suggestions_cat", params, slug = category)

    def status_friends(self, *a, **b):
        self.friends(*a, **b)
    def friends(self, user = "", is_screen_name = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("statuses", "friends", params)
    
    def status_followers(self, *a, **b):
        self.friends(*a, **b)
    def followers(self, user = "", is_screen_name = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("statuses", "followers", params)
    
    #
    # Lists Methods
    #
    def lists_create(self, name, **params):
        params["name"] = name
        return self._api("lists", "create", params)
    
    def lists_update(self, _id, **params):
        return self._api("lists", "update", params, id = _id)
    
    def lists_index(self, user = "", **params):
        return self._api("lists", "index", params, user = user)
    
    def lists_show(self, _id, user = "", **params):
        return self._api("lists", "show", user = user, id = _id)
    
    def lists_destroy(self, _id, **params):
        return self._api_delete("lists", "destroy", 
                                id = _id, params = params)
    
    def lists_statuses(self, list_id, user = "", auth = False, **params):
        return self._api("lists", "statuses", params, noauth = not auth,
                         user = user, list_id = list_id)
    
    def lists_memberships(self, user = "", **params):
        return self._api("lists", "memberships", params, user = user)
    
    def lists_subscriptions(self, user = "", **params):
        return self._api("lists", "subscriptions", params, user = user)
    
    #
    # Lists Members Methods
    #
    def lists_mlist(self, list_id, user = "", **params):
        return self._api("lists", "mlist", params, 
                         user = user, list_id = list_id)
    
    def lists_madd(self, member, list_id, user = "", **params):
        params["id"] = member
        return self._api("lists", "madd", params, 
                         user = user, list_id = list_id)

    def lists_mremove(self, member, list_id, user = "", **params):
        params["id"] = member
        return self._api("lists", "mremove", params, 
                         user = user, list_id = list_id)
    
    def lists_mshow(self, _id, list_id, user = "", **params):
        return self._api("lists", "mshow", params,
                         user = user, list_id = list_id, id = _id)

    #
    # List Subscribers Methods
    #
    def lists_slist(self, list_id, user = "", **params):
        return self._api("lists", "slist", params, 
                         user = user, list_id = list_id)
    
    def lists_sadd(self, list_id, user = "", **params):
        return self._api("lists", "sadd", params, 
                         user = user, list_id = list_id)
    
    def lists_sremove(self, list_id, user = "", **params):
        return self._api("lists", "sremove", params, 
                         user = user, list_id = list_id)
    
    def lists_sshow(self, _id, list_id, user = "", **params):
        return self._api("lists", "sshow", params,
                         user = user, list_id = list_id, id = _id)
    
    #
    # Direct Message Methods
    #
    def dm_list(self, **params):
        return self._api("dm", "list", params)

    def dm_sent(self, **params):
        return self._api("dm", "sent", params)
    
    def dm_destroy(self, _id, **params):
        return self._api("dm", "destroy", id = _id)

    def dm_new(self, user, text, **params):
        params["user"] = user
        params["text"] = text
        return self._api("dm", "new", params)

    #
    # Friendships Methods
    #
    def friends_create(self, user, **params):
        return self._api("friendship", "create", params, user = user)

    def friends_destroy(self, user, **params):
        return self._api("friendship", "destroy", params, user = user)

    def friends_exists(self, user_a, user_b, auth = False, **params):
        print >>sys.stderr, "[warning] Hey there: Why not try the friendships/show method?"
        params["user_a"] = user_a
        params["user_b"] = user_b
        return self._api("friendship", "exists", params, noauth = not auth)
    
    def friends_show(self, target, source = "",
                     is_screen_name = False, auth = False, **params):
        tp = ("target_id", "target_screen_name")
        params[self._idtype(target, tp, is_screen_name = is_screen_name)] = target
        
        sp = ("source_id", "source_screen_name")
        params[self._idtype(source, sp, is_screen_name = is_screen_name)] = source
        
        return self._api("friendship", "show", params, noauth = not auth)

    def friends_incoming(self, **params):
        return self._api("friendship", "incoming", params)

    def friends_outgoing(self, **params):
        return self._api("friendship", "outgoing", params)
    
    #
    # Social Graph Methods
    #
    def friends_ids(self, user = "",
                    is_screen_name = False, auth = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("friendship", "friends", params, noauth = not auth)
    
    def followers_ids(self, user = "",
                      is_screen_name = False, auth = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("friendship", "followers", params, noauth = not auth)

    #
    # Account Methods
    #
    def verify_credentials(self, **params):
        return self._api("account", "verify_credentials")

    def rate_limit(self, ip_limit = False, **params):
        # ip_limit: True: IP Limit, False: Account Limit
        return self._api("account", "rate_limit", noauth = ip_limit)
    
    def end_session(self, **params):
        return self._api("account", "end_session")

    def delivery_device(self, device, **params):
        params["device"] = device
        return self._api("account", "delivery_device", params)

    def profile_colors(self, **params):
        return self._api("account", "profile_colors", params)

    def profile_image(self, image, **params):
        params["image"] = image
        return self._api("account", "profile_image", params)

    def profile_background_image(self, image, **params):
        params["image"] = image
        return self._api("account", "profile_back", params)

    def profile(self, **params):
        return self._api("account", "update_profile", params)
    
    #
    # Favorites Method
    #
    def favorites(self, user = "", **params):
        return self._api("favorite", "list", params, user = user)

    def favorite_create(self, _id = "", **params):
        return self._api("favorite", "create", params, id = _id)

    def favorite_destroy(self, _id = "", **params):
        return self._api("favorite", "destroy", params, id = _id)

    #
    # Notification Methods
    #
    def notification_follow(self, **params):
        pass
    def notification_leave(self, **params):
        pass

    #
    # Block Methods
    #
    def block_create(self, user, is_screen_name = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("block", "create", params)

    def block_destroy(self, user, is_screen_name =  False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("block", "destroy", params)

    def block_exists(self, user, is_screen_name = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("block", "destroy", params)

    def block_list(self, **params):
        return self._api("block", "blocking", params)

    def block_ids(self, **params):
        return self._api("block", "ids", params)

    def report_spam(self, user, is_screen_name = False, **params):
        params[self._idtype(user, is_screen_name = is_screen_name)] = user
        return self._api("block", "report_spam", params)

    #
    # Saved Searches Methods
    #
    def saved_searches(self): pass
    def saved_searches_show(self): pass
    def saved_searches_create(self): pass
    def saved_searches_destroy(self): pass
    
    #
    # Local Trends Methods
    #
    def trends_available(self): pass
    def trends_location(self): pass

if __name__ == "__main__":
    import sys

    api = api(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    print api.user["screen_name"]
    for status in api.home_timeline(count = 10):
        print "%15s: %s" % (
            status["user"]["screen_name"], status["text"])
