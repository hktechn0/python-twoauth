import urllib2
import xml.parsers.expat

# XML Parser for Twitter API

class twitterxml:
    def __init__(self, xmlstr):
        # stack
        self.name = []
        self.data = []
        self.cdata = ""

        # mode stack
        self.mode = []
        self.nmode = ""
        
        # XML Parser
        self.p = xml.parsers.expat.ParserCreate()
        self.p.StartElementHandler = self.start_element
        self.p.CharacterDataHandler = self.char_data
        self.p.EndElementHandler = self.end_element
        self.p.Parse(xmlstr)
    
    def start_element(self, name, attrs):
        # push element name
        self.name.append(name)
        self.mode.append(self.nmode)
        self.cdata = ""
        self.nmode = ""
        
        # type="array" mode check
        if attrs:
            for a in attrs:
                if a == "type" and attrs["type"] == "array":
                    self.nmode = "array"
                    break

        if name == "ids":
            self.nmode = "array"
    
    def end_element(self, name):
        # character data strip
        cdata = self.cdata.strip(" \n")

        # pop mode and set next mode
        mode = self.mode.pop()
        self.nmode = mode

        if cdata:
            if mode:
                # for ids
                self.data.append(cdata)
                self.cdata = ""
            else:
                # string element
                self.data.append([name, cdata])
                self.cdata = ""
        elif self.name and name == self.name[-1]:
            # empty element
            self.data.append([name, ""])
        else:
            elements = []
            while self.name.pop() != name:
                elements.append(self.data.pop())

            self.name.append(name)

            if mode:
                # array element
                self.data.append(dict(elements))
            else:
                if isinstance(elements[0], dict):
                    # array parent
                    self.data.append((name, elements))
                else:
                    # others
                    try:
                        self.data.append((name, dict(elements)))
                    except ValueError:
                        # for ids
                        self.data.append((name, tuple(elements)))
    
    def char_data(self, c):
        self.cdata += c

def xmlparse(xml_text):
    parsed = twitterxml(xml_text)
    parsed.data = parsed.data[0][1]
    
    return parsed.data

if __name__ == '__main__':
    #url = 'http://twitter.com/statuses/public_timeline.xml'
    url = 'http://twitter.com/statuses/user_timeline.xml?screen_name=hktechno'
    xml_tl = urllib2.urlopen(url).read()

    tl = xmlparse(xml_tl)

    for post in tl:
        print "@%s\t%s" % (post["user"]["screen_name"], post["text"])
