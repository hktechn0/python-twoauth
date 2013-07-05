#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib2
import urlparse
import urllib
import json
import threading

import oauth
import status
import event

from __init__ import __version__

# Streaming API Stream class
class Stream(threading.Thread):
    def __init__(self, request):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.request = request
        
        self._hose = None
        self._buffer = unicode()
        self._lock = threading.Lock()
        self.event = threading.Event()
        self.die = False
    
    @property
    def is_connected(self):
        return bool(self._hose) and bool(self._hose.fp)
    
    def _get_delimited(self):
        # tooooooooo slow (maybe readline() has big buffer)
        # while delimited == "":
        #    delimited = hose.readline().strip()
        
        delimited = unicode()
        c = unicode()
        
        # get delimited (number of bytes that should be read
        while not (delimited != "" and c == "\n"):
            try:
                c = self._hose.read(1)
                delimited += c.strip()
            except:
                c = None
            
            # EOF (disconnected)
            if not c: return
            # destroy
            if self.die: return
        
        return int(delimited)
    
    def run(self):
        try:
            self._hose = urllib2.urlopen(self.request)
        except:
            self.event.set()
            return
        
        while not self.die:
            read_bytes = self._get_delimited()
            if self.die: break
            
            # maybe stream disconnected
            if read_bytes == None:
                break
            
            # read stream
            self._lock.acquire()
            self._buffer += self._hose.read(read_bytes)
            self._lock.release()
            
            self.event.set()
        
        # connection close before finish thread
        self._hose.close()
        self.event.set()
    
    def read(self):
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
        
        return json_str
    
    # pop statuses
    def pop(self):
        self.event.clear()
        
        text = self.read()
        if not text: return []
        
        statuses = []
        
        for i in map(json.loads, text.strip().split("\n")):
            if "text" in i:
                i = status.TwitterStatus(i)
            elif "event" in i:
                i = event.TwitterEvent(i)
            
            statuses.append(i)
        
        return statuses
    
    def stop(self):
        self.die = True

# Streaming API class
class StreamingAPI(object):
    useragent = "python-twoauth v%s" % (__version__)
    
    def __init__(self, oauth, useragent = None):
        self.oauth = oauth
        
        if not useragent:
            self.useragent = useragent
    
    def _request(self, path, method = "GET", params = {}):    
        # added delimited, stall_warnings parameter
        params["delimited"] = "length"
        params["stall_warnings"] = True
        req = self.oauth.oauth_request(path, method, params)
        
        # User Agent Header
        req.add_header("X-User-Agent", self.useragent)
        
        return req
    
    def _params(self, follow, locations, track):
        params = dict()
        
        # Parameters are logical OR
        if follow:
            params["follow"] = u",".join([str(int(i)) for i in follow])
        if locations:
            params["locations"] = u",".join([str(float(i)) for i in locations])
        if track:
            params["track"] = u",".join([unicode(i).strip() for i in track]).encode("utf-8")
        
        return params
    
    def sample(self):
        path = "https://stream.twitter.com/1.1/statuses/sample.json"
        return Stream(self._request(path))
    
    def filter(self, follow = [], locations = [], track = [], **params):
        path = "https://stream.twitter.com/1.1/statuses/filter.json"
        p = self._params(follow, locations, track)
        p.update(params)
        
        return Stream(self._request(path, "POST", p))
    
    def user(self, follow = [], locations = [], track = [], **params):
        path = "https://userstream.twitter.com/2/user.json"
        p = self._params(follow, locations, track)
        #p["with"] = params.get("with_", dict())
        p.update(params)
        
        return Stream(self._request(path, "POST", p))
