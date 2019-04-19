import json

class typeDimmer:
    keyWords = {
        "ein" : 1,
        "an" : 1,
        "aus" : 0,
        "ab" : 0,
        "auf" : 2,
        "zu" : 2
    }

    def __init__(self,name,client):
        self.name = name
        self.client = client

    def parseCMD(self,cmd):
        keyWord = list()
        numWord = int()
        for key in cmd:
            if key in self.keyWords:
                keyWord.append(self.keyWords[key])
            elif key.isdigit():
                numWord = int(key)
        if numWord and (2 in keyWord):
            self.__setDim(numWord)
        elif 0 in keyWord:
            self.__turnOff()
        elif 1 in keyWord:
            self.__turnOn()

    def subscribe(self,topic):
        if topic.endswith("/"):
            self.client.subscribe(topic + self.name.lower() + "/lum")
        else:
            self.client.subscribe((topic + "/" + self.name.lower() + "/lum", 1))

    def appCMD(self, topic, payload):
        if "lum" in topic:
            self.__setDim(payload)

    def __turnOn(self):
        cmd = dict(cmd = dict(brightness = 100))
        self.__send(cmd)

    def __turnOff(self):
        cmd = dict(cmd = dict(brightness = 0))
        self.__send(cmd)

    def __setDim(self,lum):
        cmd = dict(cmd = dict(brightness = lum))
        self.__send(cmd)

    def __send(self,cmd):
        self.client.publish("/actu/" + self.name + "/cmd",json.dumps(cmd))
