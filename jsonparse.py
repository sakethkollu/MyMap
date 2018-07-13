import json
import datetime

import matplotlib


from pprint import pprint

with open("data/Location History.json") as f:
    data = json.load(f)

def getTimeStamp(index):
    return data["locations"][index]["timestampMs"]

def getUTCTime(millis):
    return datetime.datetime.fromtimestamp(float(millis)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')

def getCoordinate(index):
    return [float(data["locations"][index]["longitudeE7"]) / 10000000
        , float(data["locations"][index]["latitudeE7"])/ 10000000]

DATAPOINTS = len(data["locations"])
for i in range(0, 10):
    print(getUTCTime(getTimeStamp(i)))#.locations[0].timestampMs)

