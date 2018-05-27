import utils

from pylab import *

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
gAccount = 100000
gAmount = 0
gStop = None
buyDict = {}
sellDict = {}

#--------functions--------
def plotData():
    t = arange(0.0, len(closeList), 1)
    th = arange(0.0, len(donchianHigh), 1)
    markers_buy_x = buyDict.keys()
    markers_buy_y = []
    for i in buyDict.keys():
        markers_buy_y.append(buyDict[i]*1.1)
    markers_sell_x = buyDict.keys()
    markers_sell_y = []
    for i in sellDict.keys():
        markers_sell_y.append(sellDict[i] * 0.9)

    plt.plot(t, closeList, '-', color="orange", markersize=2)
    #plt.plot(t, highList, '-', color="yellow", markersize=1)
    #plt.plot(t, lowList, '-', color="yellow", markersize=1)
    plt.plot(t, donchianHigh, '-', color="blue", markersize=1)
    plt.plot(t, donchianLow, '-', color="blue", markersize=1)
    plt.plot(markers_buy_x, markers_buy_y, 'v', color="green")
    plt.plot(markers_sell_x, markers_sell_y, 'v', color="red")
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
#utils.saveData("dhighFile"+str(STOPDAYS*TIMEBASE),donchianHigh)
#utils.saveData("dlowFile"+str(STOPDAYS*TIMEBASE),donchianLow)

#---buy and sell---
index = 0
for element in closeList:
    if ((index > (DONCHIANDAYS*TIMEBASE+STOPDAYS))and (gAmount == 0)):
        if (utils.checkLong(element, donchianHigh,index,TIMEBASE)):
            buyLong(AMOUNTOFCONTRACTS,element,FEE,1234, index)
            print ("INDEX = "+ str(index))
    index = index + 1

plotData()

#todo:
#Stop richtig setzen in buy Funktion
#sell einfügen in main buy and sell