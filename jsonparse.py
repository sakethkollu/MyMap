import json
import datetime
import platform
import pandas as pd
import pprint

class MapData:

    global DATAFILE
    global DATAPOINTS
    global PARSEDJSON
    global DATAFRAME

    def __init__(self, JSON):
        self.DATAFILE = JSON
        self.PARSEDJSON = self.parseJSON()
        self.DATAPOINTS = self.getJSONLength()
        self.extractLatitudeToColumn()
        self.extractLongitudeToColumn()
        self.extractMillisToColumn()
        self.convertMillisToDateToColumn()

       # self.PARSEDJSON = self.PARSEDJSON.drop(labels=['locations'], axis=1, inplace=False)

    def printGlobals(self):
        try:
            print("DATAFILE", self.DATAFILE)
            print("DATAPOINTS", self.DATAPOINTS)
            print("PARSEDJSON", self.PARSEDJSON)
        except AttributeError:
            print("All globals may not be defined...")

    def parseJSON(self):
        return pd.read_json(self.DATAFILE)

    def getJSONLength(self):
        return len(self.PARSEDJSON)

    def extractLatitudeToColumn(self):
        self.PARSEDJSON['latitudes'] = self.PARSEDJSON['locations'].map(lambda x: float(x['latitudeE7'])) / (10.**7)

    def extractLongitudeToColumn(self):
        self.PARSEDJSON['longitudes'] = self.PARSEDJSON['locations'].map(lambda x: float(x['longitudeE7'])) / (10.**7)

    def extractMillisToColumn(self):
        self.PARSEDJSON['millis'] = self.PARSEDJSON['locations'].map(lambda x: float(x['timestampMs']))

    def convertMillisToDateToColumn(self):
        self.PARSEDJSON['date'] = self.PARSEDJSON['millis'].map(lambda x: self.getUTCTime(x))

    def getUTCTime(self, millis):
        return datetime.datetime.fromtimestamp(float(millis)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')

    def getPositionAtTime(self, millis):
        return self.PARSEDJSON[self.PARSEDJSON['latitudes'].notnull() & (self.PARSEDJSON['millis'] > millis)]




if __name__ == '__main__':
    sakethData = MapData("data/Location History.json")
    print(sakethData.getPositionAtTime(152858000000))