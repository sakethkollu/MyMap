from math import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np
import platform
import tkinter as tk
from tkinter import *
from mpl_toolkits.basemap import Basemap
from jsonparse import MapData
#determines OS, and changes font depending on OS

fontName = "Segoe UI"

fontSize = 10
TickFont = {'fontname':fontName}
TickFontSize = 10


#declares the graph
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





app = 0
iterations = 0

#update function, run regularly to update according to changes on the GUI
def animate(i):
    global app

    global iterations


    print("creating map", iterations)
    sakethData = MapData("data/Location History.json")

    m = Basemap(width=12000000, height=9000000, projection='lcc',
                resolution='i', lat_1=50., lat_2=55, lat_0=50, lon_0=-107.)
    m.drawmapboundary(color=border_color, fill_color=water_color)
    m.drawcoastlines(color=coastline_color)
    m.drawcountries(color=border_color)
    m.fillcontinents(color=land_color, lake_color=water_color)
    m.drawparallels(np.arange(-90., 120., 30.), color=meridian_color)
    m.drawmeridians(np.arange(0., 420., 60.), color=meridian_color)
    x, y = m(sakethData.PARSEDJSON['longitudes'].values, sakethData.PARSEDJSON['latitudes'].values)
    m.scatter(x, y, s=8, color=marker_fill_color, edgecolor=marker_edge_color, alpha=1, zorder=3)
    iterations +=1




#Tkinter GUI
class GraphingCalculator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")

        #creates window title
        tk.Tk.wm_title(self, "Google Location Data Plotter")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        #grids the container for the rest of the elements
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frame = GraphPage(container, self)
        self.frames[GraphPage] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.configure(background = "white")
        self.show_frame(GraphPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def getFrame(self):
        return self.frame



class GraphPage(tk.Frame):
    #redeclares global within class
    global eq
    global label

    global Xmax
    global Xmin
    global xminEntry
    global xmaxEntry

    global Ymax
    global Ymin
    global yminEntry
    global ymaxEntry

    global A
    global B
    global AEntry
    global BEntry

    global Y
    global integral
    global FTC


    def __init__(self, parent, controller):

        def updateFunction(event):
            return self

        global fontName
        global fontSize


        tk.Frame.__init__(self, parent)
        #labels and entry boxes for all other inputs
        #makes function update when pressing enter on any input box
        self.mainTitleText = StringVar()
        self.mainTitleText.set('Google Map Data')
        self.mainTitle = Label(self, text=self.mainTitleText.get(), font = (fontName,16))
        self.mainTitle.configure(background = "white")
        self.mainTitle.grid(row=0, columnspan = 2)

        animate(1)

        e1 = Entry(self)
        e1.configure(background="#E0E0E0")
        e1.grid(row=2, column=1)
        e1.bind('<Return>', animate(1))

        graphingFrame = Frame(self)
        canvas = FigureCanvasTkAgg(fig, graphingFrame)

        canvas.show()
        canvas.get_tk_widget().grid(row=1)

        canvas._tkcanvas.grid(row=2)
        graphingFrame.grid(row=1, columnspan=2, sticky=W)





#creates the page, checking for changes every 250ms
app = GraphingCalculator()
#ani = animation.FuncAnimation(fig, animate, interval=500)

app.mainloop()
