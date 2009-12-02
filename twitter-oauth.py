import oauth
import twxml

import urllib, urllib2

class twoauth():
    twurl = "http://twitter.com/"
    apit = ".xml"

    url = {
        "statuses" : {
            "update" : twurl + "statuses/update" + apit,
            "friends_timeline" : twurl + "statuses/friends_timeline" + apit,
            "home_timeline" : twurl + "statuses/home_timeline" + apit
            },
        "account" : {
            "verify_credentials" : twurl + "account/verify_credentials" + apit
            }
        }

    def __init__(self, ckey, csecret, atoken, asecret,
                 oauth_obj = None):
        if oauth_obj == None:
            self.oauth = oauth.oauth(ckey, csecret, atoken, asecret)
        else:
            self.oauth = oauth_obj

        req = self.oauth.oauth_request(self.url["account"]["verify_credentials"])
        getxml = urllib2.urlopen(req).read()

        user = twxml.xmlparse(getxml)
        
        self.user = user[0]

    def _get(self, a, b):
        return twxml.xmlparse(
            urllib2.urlopen(
                self.oauth.oauth_request(
                    self.url[a][b])).read())

    def _post(self, a, b, params):
        return twxml.xmlparse(
            urllib2.urlopen(
                self.oauth.oauth_request(
                    self.url[a][b], "POST", params)).read())
    
    def friends_timeline(self):
        return self._get("statuses", "friends_timeline")

    def home_timeline(self):
        return self._get("statuses", "home_timeline")

    def status_update(self, status, reply_to = ""):
        params = { "status" : status,
                   "in_reply_to_status_id": reply_to }
        return self._post("statuses", "update", params)

if __name__ == "__main__":
    api = twoauth("vf5Y4VMP0ktRLaoXKPMFDQ",
            "IvX8diWHfVGYpjeYIhTkybR9IEhxoYJv7T12cUk",
            "",
            "")
    
    print api.user["screen_name"]

    print "What are you doing?:",
    post = raw_input()
    print api.status_update(post)

    for status in api.home_timeline():
        print "%15s: %s" % (
            status["user"]["screen_name"], status["text"])
