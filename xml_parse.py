import urllib2
import xml.parsers.expat

class tw_xmlparse:
    def __init__(self, xmlstr):
        self.tmps = ""
        self.p = xml.parsers.expat.ParserCreate()
        self.p.StartElementHandler = self.mode_init
        self.p.CharacterDataHandler = self.char_data
        self.p.Parse(xmlstr)
    
    def mode_init(self, name, attrs):
        if name == "statuses":
            self.p.StartElementHandler = self.status_init
            self.statuses = []

    def status_init(self, name, attrs):
        if name == "status":
            self.status = []
            self.p.StartElementHandler = self.status_start
            self.p.EndElementHandler = self.status_end

    def status_start(self, name, attrs):
        self.tmps = ""
        if name == "user":
            self.user = []
            self.p.StartElementHandler = self.user_start
            self.p.EndElementHandler = self.user_end

    def user_start(self, name, attrs):
        self.tmps = ""

    def user_end(self, name):
        if name == "user":
            self.status.append(["user", dict(self.user)])
            self.p.StartElementHandler = self.status_start
            self.p.EndElementHandler = self.status_end
        else:
            self.user.append([name, self.tmps])

    def status_end(self, name):
        if name == "status":
            self.statuses.append(dict(self.status))
            self.p.StartElementHandler = self.status_init
        else:
            self.status.append([name, self.tmps])

    def end_element(self, name):
        pass

    def char_data(self, data):
        self.tmps += data

if __name__ == '__main__':
    #url = 'http://twitter.com/statuses/public_timeline.xml'
    url = 'http://twitter.com/statuses/user_timeline.xml?screen_name=hktechno'
    xml_tl = urllib2.urlopen(url).read()

    tl = tw_xmlparse(xml_tl)
    
    for post in tl.statuses:
        print "@%s\t%s" % (post["user"]["screen_name"], post["text"])
