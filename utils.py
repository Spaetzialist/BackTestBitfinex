import pickle
from pylab import *

def buildDonchian(numberOfCandles, high, low):
    donchianHighList = []
    donchianLowList = []
    for i in range(0, len(high)):
        if (i>=numberOfCandles-1):
            donchianHighList.append(max(high[i-numberOfCandles+1:i+1]))
            donchianLowList.append(min(low[i - numberOfCandles+1:i+1]))
        else:
            donchianHighList.append(0)
            donchianLowList.append(0)
        if (i%10000 == 0):
            print (i)
    return donchianHighList,donchianLowList


def fillLists(l):
    closeList = []
    highList = []
    lowList = []
    for e in l:
        closeList.append(float(e[2]))
    for e in l:
        highList.append(float(e[3]))
    for e in l:
        lowList.append(float(e[4]))
    return closeList, highList, lowList

def saveData(file,data):
    # Store data (serialize)
    with open(file, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def loadData(file):
    # Load data (deserialize)
    unserialized_data = None
    with open(file, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data

def plotData(data):
    t = arange(0.0, len(data), 1)
    plt.plot(t, data, '-', color="orange", markersize=2)
    plt.show()

def checkLong(close, highList,index, timebase):
    if (close > highList[int(index/timebase)*timebase]):
        return True
    else:
        return False

def setStopLow(donchianLowStop,index, stopdays, timebase):
    if ((index > stopdays * timebase) and (index < len(donchianLowStop))):
        ticksAktuelleCandle = index % timebase
        ticksLetzteXCandles = stopdays * timebase
        stopLow = min(donchianLowStop[index - ticksAktuelleCandle - ticksLetzteXCandles:index - ticksAktuelleCandle])
        return stopLow
    else:
        return -1