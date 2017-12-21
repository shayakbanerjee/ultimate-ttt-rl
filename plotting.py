__author__ = 'Shayak'
import vincent
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np

def drawXYPlotByFactor(dataDict, xlabel='', ylabel='', legend=None,
                       title=None, logy=False, location=5):
    # Assuming that the data is in the format { factor: [(x1, y1),(x2,y2),...] }
    PLOT_STYLES = ['r^-', 'bo-', 'g^-', 'ks-', 'ms-', 'co-', 'y^-']
    styleCount = 0
    displayedPlots = []
    pltfn = plt.semilogy if logy else plt.plot
    for factor in dataDict:
        xpoints = [a[0] for a in dataDict[factor]]
        ypoints = [a[1] for a in dataDict[factor]]
        displayedPlots.append(pltfn(xpoints, ypoints, PLOT_STYLES[styleCount]))
        styleCount = min(styleCount+1, len(PLOT_STYLES)-1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if legend is None:
        plt.legend(dataDict.keys(), loc=location)
    else:
        plt.legend(legend, loc=location)
    if title is not None:
        plt.title(title)
    plt.show()
