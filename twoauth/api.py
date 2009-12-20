import urllib, urllib2

import oauth
import twitterxml

#
# OAuth supported Twitter library for Python
# - Hirotaka Kawata (@hktechno)
# - info@techno-st.net
# - http://www.techno-st.net/
#

class api():
    twurl = "http://twitter.com/"
    apiurl = "http://api.twitter.com/1/"
    api_t = ".xml"
    
    url = {
        "statuses" : {
            "public_timeline"  : twurl + "statuses/public_timeline" + api_t,
            "home_timeline"    : apiurl + "statuses/home_timeline" + api_t,
            "friends_timeline" : twurl + "statuses/friends_timeline" + api_t,
            "user_timeline"    : twurl + "statuses/user_timeline" + api_t,
            "mentions"         : twurl + "statuses/mentions" + api_t,
            "retweeted_by_me"  : apiurl + "statuses/retweeted_by_me" + api_t,
            "retweeted_to_me"  : apiurl + "statuses/retweeted_to_me" + api_t,
            "retweets_of_me"   : apiurl + "statuses/retweets_of_me" + api_t,
            "show"             : twurl + "statuses/show/" + "%id%" + api_t,
            "update"           : twurl + "statuses/update" + api_t,
            "destroy"          : twurl + "statuses/destroy/" + "%id%" + api_t,
            "retweet"          : apiurl + "statuses/retweet/" + "%id%" + api_t,
            "retweets"         : apiurl + "statuses/retweets/" + "%id%" + api_t,
            "friends"          : twurl + "statuses/friends" + api_t,
            "followers"        : twurl + "statuses/followers" + api_t
            },
        "users" : {
            "show"   : twurl + "users/show" + api_t,
            "search" : apiurl + "users/search" + api_t
            },
        "account" : {
            "verify_credentials" : twurl + "account/verify_credentials" + api_t,
            "rate_limit"      : twurl + "account/rate_limit_status" + api_t,
            "end_session"     : twurl + "account/end_session" + api_t,
            "delivery_device" : twurl + "account/update_delivery_device" + api_t,
            "profile_colors"  : twurl + "account/update_profile_colors" + api_t,
            "profile_image"   : twurl + "account/update_profile_image" + api_t,
            "profile_back"    : twurl + "account/update_profile_background_image" + api_t,
            "update_profile"  : twurl + "account/update_profile" + api_t,
            },
        "lists" : {
            "create"        : apiurl + "%user%/lists" + api_t,
            "update"        : apiurl + "%user%/lists/%id%" + api_t,
            "index"         : apiurl + "%user%/lists" + api_t,
            "show"          : apiurl + "%user%/lists/%id%" + api_t,
            "destroy"       : apiurl + "%user%/lists/%id%" + api_t,
            "statuses"      : apiurl + "%user%/lists/%id%/statuses" + api_t,
            "memberships"   : apiurl + "%user%/lists/memberships" + api_t,
            "subscriptions" : apiurl + "%user%/lists/subscriptions" + api_t,
            "mlist"    : apiurl + "%user%/%id%/members" + api_t,
            "madd"     : apiurl + "%user%/%id%/members" + api_t,
            "mremove"  : apiurl + "%user%/%id%/members" + api_t,
            "mshow"    : apiurl + "%user%/%list_id%/members/%id%" + api_t,
            },
        "dm" : {
            "list"    : twurl + "direct_messages" + api_t,
            "sent"    : twurl + "direct_messages/sent" + api_t,
            "new"     : twurl + "direct_messages/new" + api_t,
            "destroy" : twurl + "direct_messages/destroy/" + "%id%" + api_t,
            },
        "friendship" : {
            "create"  : twurl + "friendships/create/%user%" + api_t,
            "destroy" : twurl + "friendships/destroy/%user%" + api_t,
            "exists"  : twurl + "friendships/exists" + api_t,
            "show"    : twurl + "friendships/show" + api_t,
            },
        "favorite" : {
            "list"    : twurl + "favorites/%user%" + api_t,
            "create"  : twurl + "favorites/create/%id%" + api_t,
            "destroy" : twurl + "favorites/destroy/%id%" + api_t,
            },
        }

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
            },
        "favorite" : {
            "list"    : "GET",
            "create"  : "POST",
            "destroy" : "POST",
            },
        }

    def __init__(self, ckey, csecret, atoken, asecret,
                 oauth_obj = None):
        if oauth_obj == None:
            self.oauth = oauth.oauth(ckey, csecret, atoken, asecret)
        else:
            self.oauth = oauth_obj

        req = self.oauth.oauth_request(
            self.url["account"]["verify_credentials"])
        getxml = urllib2.urlopen(req).read()

        user = twitterxml.xmlparse(getxml)
        self.user = user
    
    def _api(self, a, b, params = {}, noauth = False, **replace):
        url = self._urlreplace(a, b, replace)
        method = self.method[a][b]
        params = self._rm_noparams(params)
        
        if noauth:
            # try no auth request
            try:
                return self._api_noauth(url, params)
            except urllib2.HTTPError, e:
                if e.code == 403:
                    pass
                else:
                    raise
        
        req = self.oauth.oauth_request(url, method, params)
        xml = urllib2.urlopen(req).read()
        return twitterxml.xmlparse(xml)
    
    def _api_noauth(self, url, params):
        # No use OAuth, GET only
        paramstr = urllib.urlencode(params)
        xml = urllib2.urlopen("%s?%s" % (url, paramstr)).read()
        return twitterxml.xmlparse(xml)
    
    def _api_delete(self, a, b, user = "", _id = "", params = {}):
        if not user:
            user = self.user["screen_name"]
        
        url = self.url[a][b]
        url = url.replace("%user%", str(user))
        url = url.replace("%id%", str(_id))
        
        params = self._rm_noparams(params)
        res = self.oauth.oauth_http_request(url, "DELETE", params)
        return twitterxml.xmlparse(res.read())
    
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

    def _idtype(self, uid, ret = ("user_id", "screen_name")):
        if str(uid).isdigit():
            # numeric id
            return ret[0]
        else:
            # screen_name
            return ret[1]

    def _urlreplace(self, a, b, replace):
        url = self.url[a][b]

        if "user" not in replace or not replace["user"]:
            replace["user"] = self.user["screen_name"]

        for d in replace:
            url = url.replace("%%%s%%" % d, str(replace[d]))

        return url
    
    #
    # Timeline Methods
    #
    def public_timeline(self):
        return self._api("statuses", "public_timeline", noauth = True)
    
    def home_timeline(self, **params):
        return self._api("statuses", "home_timeline", params)
    
    def friends_timeline(self, **params):
        return self._api("statuses", "friends_timeline", params)

    def user_timeline(self, user = "", **params):
        params[self._idtype(user)] = user
        data = self._api("statuses", "user_timeline", params, noauth = True)
        return data
    
    def mentions(self, **params):
        return self._api("statuses", "mentions", params)
    
    def rt_by_me(self, **params):
        return self._api("statuses", "retweeted_by_me", params)
    
    def rt_to_me(self, **params):
        return self._api("statuses", "retweeted_to_me", params)
    
    def rt_of_me(self, **params):
        return self._api("statuses", "retweets_of_me", params)
    
    #
    # Status Methods
    #
    def status_show(self, _id):
        return self._api("statuses", "show", noauth = True, id = _id)
    
    def status_update(self, status, **params):
        params["status"] = status
        return self._api("statuses", "update", params)
    
    def status_destroy(self, _id):
        return self._api("statuses", "destroy", id = _id)
    
    def status_retweet(self, _id):
        return self._api("statuses", "retweet", id = _id)
    
    def status_retweets(self, _id):
        return self._api("statuses", "retweets", id = _id)
    
    #
    # User Methods
    #
    def user_show(self, user, **params):
        params[self._idtype(user)] = user
        return self._api("users", "show", params, noauth = True)
    
    def user_search(self, q, **params):
        params["q"] = q
        return self._api("users", "search", params)
    
    def status_friends(self, user = "", **params):
        params[self._idtype(user)] = user
        return self._api("statuses", "friends", params)
    
    def status_followers(self, user = "", **params):
        params[self._idtype(user)] = user
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
                                _id = _id, params = params)
    
    def lists_statuses(self, _id, user = "", **params):
        return self._api("lists", "statuses", params, noauth = True,
                         user = user, id = _id)
    
    def lists_memberships(self, user = "", **params):
        return self._api("lists", "memberships", params, user = user)
    
    def lists_subscriptions(self, user = "", **params):
        return self._api("lists", "subscriptions", params, user = user)
    
    #
    # Lists Members Methods
    #
    def lists_mlist(self, _id, user = "", **params):
        return self._api("lists", "mlist", params, user = user, id = _id)
    
    def lists_madd(self, member, _id, user = "", **params):
        params["id"] = member
        return self._api("lists", "madd", params, user = user, id = _id)

    def lists_mremove(self, member, _id, user = "", **params):
        params["id"] = member
        return self._api("lists", "mremove", params, user = user, id = _id)
    
    def lists_mshow(self, _id, list_id, user = "", **params):
        return self._api("lists", "mshow", params,
                         user = user, list_id = list_id, id = _id)

    #
    # List Subscribers Methods
    #
    def lists_slist(self):
        pass
    def lists_sadd(self):
        pass
    def lists_sremove(self):
        pass
    def lists_sshow(self):
        pass
    
    #
    # Direct Message Methods
    #
    def dm_list(self, **params):
        return self._api("dm", "list", params)

    def dm_sent(self, **params):
        return self._api("dm", "sent", params)
    
    def dm_destroy(self, _id):
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

    def friends_exists(self, user_a, user_b, **params):
        params["user_a"] = user_a
        params["user_b"] = user_b
        return self._api("friendship", "exists", params, noauth = True)
    
    def friends_show(self, target, source = "", **params):
        tp = ("target_id", "target_screen_name")
        params[self._idtype(target, tp)] = target
        
        sp = ("source_id", "source_screen_name")
        params[self._idtype(source, sp)] = source
        
        return self._api("friendship", "show", params, noauth = True)

    #
    # Social Graph Methods
    #

    #
    # Account Methods
    #
    def verify_credentials(self):
        return self._api("account", "verify_credentials")

    def rate_limit(self, ip_limit = False):
        # ip_limit: True: IP Limit, False: Account Limit
        return self._api("account", "rate_limit", noauth = ip_limit)
    
    def end_session(self):
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

if __name__ == "__main__":
    import sys

    api = api(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    print api.user["screen_name"]
    for status in api.home_timeline(count = 10):
        print "%15s: %s" % (
            status["user"]["screen_name"], status["text"])
