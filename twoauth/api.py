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
            "verify_credentials" : twurl + "account/verify_credentials" + api_t
            },
        "lists" : {
            "create"        : apiurl + "%user%/lists" + api_t,
            "update"        : apiurl + "%user%/lists/%id%" + api_t,
            "index"         : apiurl + "%user%/lists" + api_t,
            "show"          : apiurl + "%user%/lists/%id%" + api_t,
            "destroy"       : apiurl + "%user%/lists/%id%" + api_t,
            "statuses"      : apiurl + "%user%/lists/%id%/statuses" + api_t,
            "memberships"   : apiurl + "%user%/lists/memberships" + api_t,
            "subscriptions" : apiurl + "%user%/lists/subscriptions" + api_t
            },
        "dm" : {
            "list"    : twurl + "direct_messages" + api_t,
            "sent"    : twurl + "direct_messages/sent" + api_t,
            "new"     : twurl + "direct_messages/new" + api_t,
            "destroy" : twurl + "direct_messages/destroy/" + "%id%" + api_t
            }
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
            "verify_credentials" : "GET"
            },
        "lists" : {
            "create"        : "POST",
            "update"        : "POST",
            "index"         : "GET",
            "show"          : "GET",
            "destroy"       : "DELETE",
            "statuses"      : "GET",
            "memberships"   : "GET",
            "subscriptions" : "GET"
            },
        "dm" : {
            "list"    : "GET",
            "sent"    : "GET",
            "new"     : "POST",
            "destroy" : "POST"
            }
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
    
    def _api(self, a, b, params = {}):
        params = self._rm_noparams(params)
        xml = urllib2.urlopen(
            self.oauth.oauth_request(
                self.url[a][b],
                self.method[a][b], params)).read()
        return twitterxml.xmlparse(xml)
    
    def _api2(self, url, params = {}, method = "GET"):
        params = self._rm_noparams(params)
        xml = urllib2.urlopen(
            self.oauth.oauth_request(
                url, method, params)).read()
        return twitterxml.xmlparse(xml)

    def _api_noauth(self, a = None, b = None, params = {},
                    url = None):
        params = self._rm_noparams(params)
        paramstr = urllib.urlencode(params)
        
        if not url:
            url = self.url[a][b]
        
        xml = urllib2.urlopen("%s?%s" % (url, paramstr)).read()
        return twitterxml.xmlparse(xml)
    
    def _api_lists(self, m, user = "", _id = "", params = {}):
        if not user:
            user = self.user["screen_name"]

        url = self.url["lists"][m]
        url = url.replace("%user%", str(user))
        url = url.replace("%id%", str(_id))

        return self._api2(url, params, self.method["lists"][m])

    def _api_delete(self, a, b, user = "", _id = ""):
        if not user:
            user = self.user["screen_name"]
        
        url = self.url[a][b]
        url = url.replace("%user%", str(user))
        url = url.replace("%id%", str(_id))
        
        res = self.oauth.oauth_http_request(url, "DELETE")
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
    
    #
    # Timeline Methods
    #
    def public_timeline(self):
        return self._api_noauth("statuses", "public_timeline")

    def home_timeline(self, since_id = "", max_id = "",
                      count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "home_timeline", params)

    def friends_timeline(self, since_id = "", max_id = "",
                         count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "friends_timeline", params)

    def user_timeline(self, user_id = "", screen_name = "",
                      since_id = "", max_id = "", count = "", page = ""):
        params = { "user_id" : user_id, "screen_name" : screen_name,
                   "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        try:
            data = self._api_noauth("statuses", "user_timeline", params)
        except urllib2.HTTPError:
            data = self._api("statuses", "user_timeline", params)

        return data

    def mentions(self, since_id = "", max_id = "",
                         count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "mentions", params)
    
    def rt_by_me(self, since_id = "", max_id = "",
                 count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "retweeted_by_me", params)

    def rt_to_me(self, since_id = "", max_id = "",
                 count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "retweeted_to_me", params)

    def rt_of_me(self, since_id = "", max_id = "",
                 count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "retweets_of_me", params)

    #
    # Status Methods
    #
    def status_show(self, _id):
        url = self.url["statuses"]["show"].replace("%id%", str(_id))
        try:
            return self._api_noauth(url = url)
        except urllib2.HTTPError:
            return self._api2(url)

    def status_update(self, status, reply_to = ""):
        params = { "status" : status,
                   "in_reply_to_status_id": reply_to }
        return self._api("statuses", "update", params)

    def status_destroy(self, _id):
        return self._api2(
            self.url["statuses"]["destroy"].replace("%id%", str(_id)),
            method = self.method["statuses"]["destroy"])

    def status_retweet(self, _id):
        return self._api2(
            self.url["statuses"]["retweet"].replace("%id%", str(_id)),
            method = self.method["statuses"]["retweet"])
    
    def status_retweets(self, _id):
        return self._api2(
            self.url["statuses"]["retweets"].replace("%id%", str(_id)))

    #
    # User Methods
    #
    def user_show(self, user_id = "", screen_name = ""):
        params = { "user_id" : user_id, "screen_name" : screen_name }
        return self._api("users", "show", params)

    def user_search(self, q, par_page = "", page = ""):
        params = { "q" : q, "par_page" : par_page, "page" : page }
        return self._api("users", "search", params)

    def status_friends(self, user_id = "", screen_name = "", cursor = ""):
        params = { "user_id" : user_id, "screen_name" : screen_name,
                   "cursor" : "" }
        return self._api("statuses", "friends", params)
    
    def status_followers(self, user_id = "", screen_name = "", cursor = ""):
        params = { "user_id" : user_id, "screen_name" : screen_name,
                   "cursor" : "" }
        return self._api("statuses", "followers", params)
    
    #
    # Lists Methods
    #
    def lists_create(self, name, mode = "", description = ""):
        params = { "name" : name, "mode" : mode,
                   "description" : description }
        return self._api_lists("create", params = params)

    def lists_update(self, _id, name = "", mode = "", description = ""):
        params = { "name" : name, "mode" : mode,
                   "description" : description }
        return self._api_lists("update", _id = _id, params = params)
    
    def lists_index(self, user = "", cursor = ""):
        params = { "cursor" : cursor }
        return self._api_lists("index", user, params = params)
    
    def lists_show(self, _id, user = ""):
        return self._api_lists("show", user, _id)

    def lists_destroy(self, _id):
        return self._api_delete("lists", "destroy", _id = _id)

    def lists_statuses(self, _id, user = "",
                       since_id = "", max_id = "", count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api_lists("statuses", user, _id, params)
    
    def lists_memberships(self, user = "", cursor = ""):
        params = { "cursor" : cursor }
        return self._api_lists("memberships", user, params = params)

    def lists_subscriptions(self, user = "", cursor = ""):
        params = { "cursor" : cursor }
        return self._api_lists("subscriptions", user, params = params)
    
    #
    # List Subscribers Methods
    #

    #
    # Direct Message Methods
    #
    def dm_list(self, since_id = "", max_id = "",
            count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("dm", "list", params)

    def dm_sent(self, since_id = "", max_id = "",
            count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("dm", "sent", params)
    
    def dm_destroy(self, _id):
        return self._api2(
            self.url["dm"]["destroy"].replace("%id%", str(_id)),
            method = self.method["dm"]["destroy"])

    def dm_new(self, user, text):
        params = { "user" : user, "text" : text }
        return self._api("dm", "new", params)

if __name__ == "__main__":
    import sys

    api = api(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    print api.user["screen_name"]
    for status in api.home_timeline(count = 10):
        print "%15s: %s" % (
            status["user"]["screen_name"], status["text"])
