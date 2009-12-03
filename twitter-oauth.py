import oauth
import twxml

import urllib, urllib2

class twoauth():
    twurl = "http://twitter.com/"
    apiurl = "http://api.twitter.com/1/"
    api_t = ".xml"
    
    url = {
        "statuses" : {
            "update"           : twurl + "statuses/update" + api_t,
            "friends_timeline" : twurl + "statuses/friends_timeline" + api_t,
            "home_timeline"    : apiurl + "statuses/home_timeline" + api_t,
            "retweeted_by_me"  : apiurl + "statuses/retweeted_by_me" + api_t,
            "retweeted_to_me"  : apiurl + "statuses/retweeted_to_me" + api_t,
            "retweets_of_me"   : apiurl + "statuses/retweets_of_me" + api_t
            },
        "account" : {
            "verify_credentials" : twurl + "account/verify_credentials" + api_t
            },
        "lists" : {
            "index"       : apiurl + "%user%" + "/lists" + api_t,
            "show"        : apiurl + "%user%" + "/lists/" + "%id" + api_t,
            "memberships" : apiurl + "%user%" + "/lists/memberships" + api_t
            }
        }

    method = {
        "statuses" : {
            "update"           : "POST",
            "friends_timeline" : "GET",
            "home_timeline"    : "GET",
            "retweeted_by_me"  : "GET",
            "retweeted_to_me"  : "GET",
            "retweets_of_me"   : "GET"
            },
        "account" : {
            "verify_credentials" : "GET"
            },
        "lists" : {
            "index"       : "GET",
            "show"        : "GET",
            "memberships" : "GET"
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

        user = twxml.xmlparse(getxml)
        
        self.user = user[0]
    
    def _api(self, a, b, params):
        params = self._rm_noparams(params)
        return twxml.xmlparse(
            urllib2.urlopen(
                self.oauth.oauth_request(
                    self.url[a][b],
                    self.method[a][b], params)).read())
    
    def _api2(self, url, params, method = "GET"):
        params = self._rm_noparams(params)
        return twxml.xmlparse(
            urllib2.urlopen(
                self.oauth.oauth_request(
                    url, method, params)).read())
    
    def _api_lists(self, m, user, _id = "", params = {}):
        if not user:
            user = self.user["screen_name"]
        url = self.url["lists"][m]
        url = url.replace("%user%", user)
        url = url.replace("%id%", _id)
        return self._api2(url, params,
                          self.method["lists"][m])
    
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
    
    def friends_timeline(self, since_id = "", max_id = "",
                         count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "friends_timeline", params)
    
    def home_timeline(self, since_id = "", max_id = "",
                      count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "home_timeline", params)

    def rt_by_me(self, since_id = "", max_id = "",
                 count = "", page = ""):
        params = { "since_id" : since_id, "max_id" : max_id,
                   "count" : count, "page" : page }
        return self._api("statuses", "retweeted_by_me", params)
    
    def lists_index(self, user = None, cursor = ""):
        params = { "cursor" : cursor }
        return self._api_lists("index", user, params = params)
    
    def lists_show(self, _id, user = None):
        return self._api_lists("show", user, _id)

    def lists_memberships(self, user = None, cursor = ""):
        params = { "cursor" : cursor }
        return self._api_lists("memberships", user, params = params)
    
    def status_update(self, status, reply_to = ""):
        params = { "status" : status,
                   "in_reply_to_status_id": reply_to }
        return self._post("statuses", "update", params)

if __name__ == "__main__":
    import sys

    api = twoauth(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    print api.user["screen_name"]

#    print "What are you doing?:",
#    post = raw_input()
#    api.status_update(post)

#    for status in api.home_timeline(count = 100):
#    for status in api.rt_by_me(count = 100):
    print api.home_timeline()
    print api.lists_memberships()
#    for status in api.lists_memberships():
#        print "%15s: %s" % (
#            status["user"]["screen_name"], status["text"])
