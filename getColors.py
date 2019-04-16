import re
import string
import csv
from collections import defaultdict

devices = {
    "Nachttisch" : "typeDimmer",
    "Cube" : "typeRGB"
}

keyWords = {
    "ein" : 1,
    "an" : 1,
    "aus" : 0,
    "ab" : 0,
    "auf" : 2,
    "zu" : 2
}

seperateWords = ["und", "and"]

colorGer = dict()
colorEng = dict()

def getColors():
    with open("colorsEngGer.txt", "r",encoding='utf-8') as source:
        reader = csv.DictReader(source)
        for row in reader:
            colorGer[row['german'].lower()] = row['hex']
            colorGer[row['german']] = row['hex']
            colorGer[row['english'].lower()] = row['hex']
            colorGer[row['english']] = row['hex']
