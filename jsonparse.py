import json
import datetime
import platform
import pandas as pd
import pprint
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

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


    # define map colors
    land_color = '#f5f5f3'
    water_color = '#cdd2d4'
    coastline_color = '#f5f5f3'
    border_color = '#bbbbbb'
    meridian_color = '#f5f5f3'
    marker_fill_color = '#cc3300'
    marker_edge_color = 'None'

    # create the plot
    fig = plt.figure(figsize=(20, 10))

    # draw the basemap and its features
    m = Basemap(width=12000000, height=9000000, projection='lcc',
                resolution='i', lat_1=50., lat_2=55, lat_0=50, lon_0=-107.)
    m.drawmapboundary(color=border_color, fill_color=water_color)
    m.drawcoastlines(color=coastline_color)
    m.drawcountries(color=border_color)
    m.fillcontinents(color=land_color, lake_color=water_color)
    m.drawparallels(np.arange(-90., 120., 30.), color=meridian_color)
    m.drawmeridians(np.arange(0., 420., 60.), color=meridian_color)

    m.drawstates()
    m.bluemarble()

    # project the location history points then scatter plot them
    x, y = m(sakethData.PARSEDJSON['longitudes'].values, sakethData.PARSEDJSON['latitudes'].values)
    m.scatter(x, y, s=8, color=marker_fill_color, edgecolor=marker_edge_color, alpha=1, zorder=3)

    # show the map
    plt.show()