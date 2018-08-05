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


def buildDonchian2(days, timebase, high, low):
    donchianHighList = []
    donchianLowList = []
    numberOfCandles = int(days*timebase)
    for i in range(0, len(high)):
        if (i>numberOfCandles):
            if (i%timebase ==0):
                k = 0
                maxValue = max(high[i - numberOfCandles :i -1])
                minValue = min(low[i - numberOfCandles:i - 1])
                while (k<timebase):
                    donchianHighList.append(maxValue)
                    donchianLowList.append(minValue)
                    k = k+1
        else:
            donchianHighList.append(0)
            donchianLowList.append(0)
    return donchianHighList,donchianLowList

def setStopLow(donchianLowStop,index, stopdays, timebase):
    if ((index > stopdays * timebase) and (index < len(donchianLowStop))):
        ticksAktuelleCandle = index % timebase
        ticksLetzteXCandles = stopdays * timebase
        stopLow = min(donchianLowStop[index - ticksAktuelleCandle - ticksLetzteXCandles:index - ticksAktuelleCandle])
        #print (donchianLowStop[index - ticksAktuelleCandle - ticksLetzteXCandles:index - ticksAktuelleCandle])
        #print (ticksAktuelleCandle)
        #print (ticksLetzteXCandles)
        return stopLow
    else:
        return -1

def setStopHigh(donchianHighStop,index, stopdays, timebase):
    if ((index > stopdays * timebase) and (index < len(donchianHighStop))):
        ticksAktuelleCandle = index % timebase
        ticksLetzteXCandles = stopdays * timebase
        stopHigh = max(donchianHighStop[index - ticksAktuelleCandle - ticksLetzteXCandles:index - ticksAktuelleCandle])
        #print (donchianLowStop[index - ticksAktuelleCandle - ticksLetzteXCandles:index - ticksAktuelleCandle])
        #print (ticksAktuelleCandle)
        #print (ticksLetzteXCandles)
        return stopHigh
    else:
        return -1

def fillLists(l):
    closeList = []
    highList = []
    lowList = []
    dateList = []
    for e in l:
        dateList.append(str(datetime.datetime.fromtimestamp(e[0] / 1000)))
        closeList.append(float(e[2]))
        highList.append(float(e[3]))
        lowList.append(float(e[4]))
    return dateList,closeList, highList, lowList

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

def checkShort(close, lowList,index, timebase):
    if (close < lowList[int(index/timebase)*timebase]):
        return True
    else:
        return False
