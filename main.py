import utils

from pylab import *
from enum import Enum
#MTS    int    millisecond time stamp
#OPEN    float    First execution during the time frame
#CLOSE    float    Last execution during the time frame
#HIGH    float    Highest execution during the time frame
#LOW    float    Lowest execution during the timeframe
#VOLUME    float    Quantity of symbol traded within the timeframe

#print(l[0])
#print(l[1])
#print (str((-l[0][0]+l[1][0])/1000/60) + "min")

#--------global--------

closeList = []
highList = []
lowList = []
donchianHigh = []
donchianLow = []
donchianHighStop = []
donchianLowStop = []
gAccount = 100000000
gAmount = 0
gStop = None
buyDict = {}
stopDict = {}
sellDict = {}
class State(Enum):
    EQUAL = 0
    LONG = 1
    SHORT = 2

#--------functions--------
def plotData():
    t = arange(0.0, len(closeList), 1)

    markers_buy_x = buyDict.keys()
    markers_buy_y = []
    for i in buyDict.keys():
        markers_buy_y.append(buyDict[i]*1.05)

    markers_sell_x = sellDict.keys()
    markers_sell_y = []
    for i in sellDict.keys():
        markers_sell_y.append(sellDict[i] * 1)

    markers_stop_x = stopDict.keys()
    markers_stop_y = []
    for i in stopDict.keys():
        markers_stop_y.append(stopDict[i])

    plt.plot(t, closeList, '-', color="orange", markersize=2)
    #plt.plot(t, highList, '-', color="yellow", markersize=1)
    #plt.plot(t, lowList, '-', color="yellow", markersize=1)
    plt.plot(t, donchianHigh, '-', color="blue", markersize=1)
    plt.plot(t, donchianLow, '-', color="blue", markersize=1)
    plt.plot(t, donchianHighStop, '-', color="green", markersize=1)
    plt.plot(t, donchianLowStop, '-', color="red", markersize=1)
    plt.plot(markers_buy_x, markers_buy_y, 'v', color="green")
    plt.plot(markers_sell_x, markers_sell_y, 'x', color="red")
    plt.plot(markers_stop_x, markers_stop_y, 'x', color="black")
    #plt.xlim(0,2000)
    plt.show()


def buyLong(amount, price, fee, stop, index):
    global gAccount
    global gAmount
    global gStop

    money = amount*price*(1+(2*fee/100))
    if (money<=gAccount):
        gAccount = gAccount - amount*price*(1+(fee/100))
        gAmount = amount
        gStop = stop
        buyDict[index]=price

def sellLong(amount, price, fee, index):
    global gAccount
    global gAmount
    global gStop

    gAccount = gAccount + amount * price * (1 - (fee / 100))
    gAmount = gAmount - amount
    sellDict[index] = price

#config
AMOUNTOFCONTRACTS = 1
FEE = 0.26
DONCHIANDAYS = 7
STOPDAYS = 3
TIMEBASE = 1440
state = State.EQUAL


#--------main--------
#---load Data---
l = utils.loadData("data")
closeList, highList, lowList = utils.fillLists(l)

donchianHigh = utils.loadData("dhighFile"+str(DONCHIANDAYS*TIMEBASE))
donchianLow  = utils.loadData("dlowFile"+str(DONCHIANDAYS*TIMEBASE))
donchianHighStop = utils.loadData("dhighFile"+str(STOPDAYS*TIMEBASE))
donchianLowStop  = utils.loadData("dlowFile"+str(STOPDAYS*TIMEBASE))

#donchianHigh, donchianLow = utils.buildDonchian(DONCHIANDAYS*TIMEBASE, highList, lowList)
#donchianHighStop, donchianLowStop = utils.buildDonchian(STOPDAYS*TIMEBASE, highList, lowList)
#utils.saveData("dhighFile"+str(DONCHIANDAYS*TIMEBASE),donchianHigh)
#utils.saveData("dlowFile"+str(DONCHIANDAYS*TIMEBASE),donchianLow)
#utils.saveData("dhighFile"+str(STOPDAYS*TIMEBASE),donchianHighStop)
#utils.saveData("dlowFile"+str(STOPDAYS*TIMEBASE),donchianLowStop)

#---buy and sell---
index = 0
for price in closeList:
    #trailing Stop Long
    if (state == State.LONG):
        stop = utils.setStopLow(donchianLowStop, index, STOPDAYS, TIMEBASE)
        gStop = stop
        #stopDict[index] = stop
    #buyLong
    if ((index > (DONCHIANDAYS*TIMEBASE+STOPDAYS))and (gAmount == 0)):
        if (utils.checkLong(price, donchianHigh,index,TIMEBASE)):
            stop = utils.setStopLow(donchianLowStop,index, STOPDAYS, TIMEBASE)
            stopDict[int(index/TIMEBASE)*TIMEBASE] = stop
            buyLong(AMOUNTOFCONTRACTS,price,FEE,stop, index)
            print ("INDEX = "+ str(index))
            state = State.LONG
    index = index + 1
    #sellLong
    if ((gAmount > 0) and (price<gStop)):
        sellLong(gAmount, price, FEE, index)


plotData()

#todo:
#ta-lib integration
#Stop nachziehen
#sell einfügen in main buy and sell