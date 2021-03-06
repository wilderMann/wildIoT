import paho.mqtt.client as mqtt
import json
from getColors import *
from config import *
from typeDimmer import typeDimmer
from typeRGB import typeRGB


def on_connect(client, userdata, flags, rc):
    """Function to subscribe after connection """
    client.subscribe("/lampen/ada/json")
    for key in devices:
        if "typeDimmer" in devices[key]:
            dimm = typeDimmer(key,client)
            dimm.subscribe("/wildiot/app/")
        if "typeRGB" in devices[key]:
            rgb = typeRGB(key,client)
            rgb.subscribe("/wildiot/app/")
def on_message(client, userdata, msg):
    """Function to handle messages"""
    print(msg.topic)
    print(msg.payload)
    if msg.topic in "/lampen/ada/json":
        y = json.loads(msg.payload)
        cmd = y["data"]["value"]
        fractureString(cmd)
    if "/wildiot/app" in msg.topic:
        for key in devices:
            if key.lower() in msg.topic:
                if "typeDimmer" in devices[key]:
                    dimm = typeDimmer(key,client)
                    dimm.appCMD(msg.topic,msg.payload)
                if "typeRGB" in devices[key]:
                    rgb = typeRGB(key,client)
                    rgb.appCMD(msg.topic,msg.payload)


def fractureString(cmd):
    wordList = re.sub("[^\w]", " ",  cmd).strip().split(" ")
    commands = dict()
    i = 0
    for key in wordList:
        if key in devices:
            i += 1
            commands[i] = dict(device = key)
            commands[i]["deviceType"] = devices[key]
            commands[i]["wordList"] = list()
        elif key in seperateWords:
            i += 1
        elif i in commands:
            commands[i]["wordList"].append(key)
    print(commands)
    for key in commands:
        if "typeDimmer" in commands[key]["deviceType"]:
            dimm = typeDimmer(commands[key]["device"],client)
            dimm.parseCMD(commands[key]["wordList"])
        elif "typeRGB" in commands[key]["deviceType"]:
            rgb = typeRGB(commands[key]["device"],client)
            rgb.parseCMD(commands[key]["wordList"])

client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USR,MQTT_PW)
getColors()
client.connect(MQTT_IP,MQTT_PORT,60)


client.loop_forever()
