#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib2
import urlparse
import urllib
import json
import threading

import oauth
import status

# Streaming API Stream class
class Stream(threading.Thread):
    die = False
    _buffer = unicode()
    _lock = threading.Lock()
    event = threading.Event()
    
    def __init__(self, request):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.request = request
    
    def run(self):
        hose = urllib2.urlopen(self.request)
        
        while not self.die:
            delimited = unicode()
            
            # tooooooooo slow (maybe readline() has big buffer)
            #while delimited == "":
            #    delimited = hose.readline().strip()
            
            # get delimited (number of bytes that should be read
            while not (delimited != "" and c == "\n"):
                c = hose.read(1)
                delimited += c.strip()
                
                if c == "" or self.die:
                    hose.close()
                    return                
            
            bytes = int(delimited)
            
            # read stream
            self._lock.acquire()
            self._buffer += hose.read(bytes)
            self._lock.release()
            
            self.event.set()
            self.event.clear()
        
        # connection close before finish thread
        hose.close()
    
    # pop statuses
    def pop(self):
        json_str = None
        
        self._lock.acquire()
        try:
            json_str, self._buffer = self._buffer.rsplit("\n", 1)
        except ValueError:
            pass
        except Exception, e:
            print >>sys.stderr, "[Error] %s" % e
        finally:
            self._lock.release()
        
        if json_str == None: return []
        
        return [status.twstatus(i) if "text" in i.keys() else i
                for i in json.loads(u"[%s]" % json_str.replace("\n", ","))]
    
    def stop(self):
        self.die = True

# Streaming API class
class StreamingAPI:
    def __init__(self, oauth):
        self.oauth = oauth
    
    def _request(self, path, method = "GET", params = {}):
        host = "stream.twitter.com"
        url = "http://%s%s" % (host, path)
        
        # added delimited parameter
        params["delimited"] = "length"
        req = self.oauth.oauth_request(url, method, params)
        
        return req
    
    def sample(self):
        path = "/1/statuses/sample.json"
        return Stream(self._request(path))
    
    def filter(self, follow = [], locations = [], track = []):
        path = "/1/statuses/filter.json"
        
        params = dict()
        if follow:
            params["follow"] = urllib.quote(u",".join([unicode(i) for i in follow]).encode("utf-8"), ",")
        if locations:
            params["locations"] = urllib.quote(u",".join([unicode(i) for i in locations]).encode("utf-8"), ",")
        if track:
            params["track"] = urllib.quote(u",".join([unicode(i) for i in track]).encode("utf-8"), ",")
        
        return Stream(self._request(path, "POST", params))

if __name__ == "__main__":
    import sys

    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    
    oauth = oauth.oauth(ckey, csecret, atoken, asecret)
    
    s = StreamingAPI(oauth)
    #streaming = s.sample()
    streaming = s.filter(locations = [-122.75,36.8,-121.75,37.8,-74,40,-73,41])
    #streaming = s.filter(track = [u"spcamp", u"セプキャン"])
    
    streaming.start()
    
    while True:
        statuses = streaming.pop()
        for i in statuses:
            try:
                print i.user.screen_name, i.text
            except:
                print i

        if raw_input() == "q":
            streaming.stop()
            break
