import urllib2
import xml.parsers.expat

class twitter_xml:
    def __init__(self, xmlstr):
        self.name = []
        self.data = []
        self.cdata = ""

        self.p = xml.parsers.expat.ParserCreate()
        self.p.StartElementHandler = self.mode_init
        self.p.CharacterDataHandler = self.char_data
        self.p.EndElementHandler = self.end_element
        self.p.Parse(xmlstr)

    def mode_init(self, name, attrs):
        self.mode = name
        elem = ["statuses", "users"]
        if name in elem:
            pass
        else:
            self.name.append(name)

        self.p.StartElementHandler = self.start_element

    def start_element(self, name, attrs):
        self.name.append(name)
        self.cdata = ""

    def end_element(self, name):
        cdata = self.cdata.strip(" \n")

        if cdata:
            self.data.append([name, cdata])
            self.cdata = ""
        elif self.name and name == self.name[-1]:
            self.data.append([name, ""])
        elif not self.name and name == self.mode:
            pass
        else:
            elements = []
            while self.name.pop() != name:
                elements.append(self.data.pop())

            if len(self.name) != 0:
                self.name.append(name)
                self.data.append([name, dict(elements)])
            else:
                self.data.append(dict(elements))

    def char_data(self, c):
        self.cdata += c

def xmlparse(xml_text):
    parsed = twitter_xml(xml_text)
    return parsed.data

if __name__ == '__main__':
    #url = 'http://twitter.com/statuses/public_timeline.xml'
    url = 'http://twitter.com/statuses/user_timeline.xml?screen_name=hktechno'
    xml_tl = urllib2.urlopen(url).read()

    tl = xmlparse(xml_tl)

    for post in tl:
        print "@%s\t%s" % (post["user"]["screen_name"], post["text"])
