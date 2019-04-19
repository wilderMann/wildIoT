import json
from getColors import colorEng, colorGer, keyWords

class typeRGB:


    def __init__(self,name,client):
        self.name = name
        self.client = client

    def parseCMD(self,cmd):
        keyWord = list()
        colorWord = str()
        numWord = int()
        for key in cmd:
            if(key in keyWords):
                keyWord.append(keyWords[key])
            elif(key in colorGer):
                colorWord = colorGer[key]
            elif(key in colorEng):
                colorWord = colorEng[key]
            elif key.isdigit():
                numWord = int(key)
        if colorWord and numWord and (2 in keyWord):
            self.__setCaD(colorWord, numWord)
        elif colorWord:
            self.__setColor(colorWord)
        elif numWord and (2 in keyWord):
            self.__setDim(numWord)
        elif (0 in keyWord):
            self.__turnOff()
        elif (1 in keyWord):
            self.__turnOn()

    def subscribe(self,topic):
        if topic.endswith("/"):
            self.client.subscribe([(topic + self.name.lower() + "/rgb", 1), (topic + self.name.lower() + "/lum", 1)])
        else:
            self.client.subscribe([(topic + "/" + self.name.lower() + "/rgb", 1), (topic + "/" + self.name.lower() + "/lum", 1)])

    def appCMD(self, topic, payload):
        if "rgb" in topic:
            self.__setColor(payload)
        elif "lum" in topic:
            self.__setDim(int(payload))

    def __turnOn(self):
        cmd = dict(cmd = dict(brightness = 100))
        self.__send(cmd)

    def __turnOff(self):
        cmd = dict(cmd = dict(brightness = 0))
        self.__send(cmd)

    def __setDim(self,lum):
        cmd = dict(cmd = dict(brightness = lum))
        self.__send(cmd)

    def __setColor(self, color):
        cmd = dict(cmd = dict(color = int(color[1:],16)))
        self.__send(cmd)

    def __setCaD(self, color, lum):
        cmd = dict(cmd = dict(color = int(color[1:],16)))
        cmd["cmd"]["brightness"] = lum
        self.__send(cmd)

    def __send(self,data):
        self.client.publish("/actu/" + self.name + "/cmd",json.dumps(data))
