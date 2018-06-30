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


class State(Enum):
    EQUAL = 0
    LONG = 1
    SHORT = 2

#config
AMOUNTOFCONTRACTS = 1
FEE = 0.26
DONCHIANDAYS = 7
STOPDAYS = 3
TIMEBASE = 1440
state = State.EQUAL
STARTMONEY = 100000

#--------global--------

closeList = []
highList = []
lowList = []
donchianHigh = []
donchianLow = []
donchianHighStop = []
donchianLowStop = []
gAccountMoney = STARTMONEY   #money
gAmountAssets = 0          #assets
gStop = None
buyLongDict = {}
stopDict = {}
sellLongDict = {}
sellShortDict = {}
buyShortDict = {}
gEntryPrice = 0


#--------functions--------
def plotData():
    t = arange(0.0, len(closeList), 1)
    tD = arange(0, len(donchianHigh), 1)
    tS = arange(0, len(donchianHighStop), 1)

    markers_buy_x = buyLongDict.keys()
    markers_buy_y = []
    for i in buyLongDict.keys():
        markers_buy_y.append(buyLongDict[i]*1.05)

    markers_sell_x = sellLongDict.keys()
    markers_sell_y = []
    for i in sellLongDict.keys():
        markers_sell_y.append(sellLongDict[i] * 1)

    markers_buyShort_x = buyShortDict.keys()
    markers_buyShort_y = []
    for i in buyShortDict.keys():
        markers_buyShort_y.append(buyShortDict[i]*1.05)

    markers_sellShort_x = sellShortDict.keys()
    markers_sellShort_y = []
    for i in sellShortDict.keys():
        markers_sellShort_y.append(sellShortDict[i] * 1)

    markers_stop_x = stopDict.keys()
    markers_stop_y = []
    for i in stopDict.keys():
        markers_stop_y.append(stopDict[i])



    plt.plot(t, closeList, '-', color="orange", markersize=2)
    #plt.plot(t, highList, '-', color="yellow", markersize=1)
    #plt.plot(t, lowList, '-', color="yellow", markersize=1)
    plt.plot(tD, donchianHigh, '-', color="blue", markersize=1)
    plt.plot(tD, donchianLow, '-', color="blue", markersize=1)
    plt.plot(tS, donchianHighStop, '-', color="green", markersize=1)
    plt.plot(tS, donchianLowStop, '-', color="red", markersize=1)
    plt.plot(markers_buy_x, markers_buy_y, 'v', color="green")
    plt.plot(markers_sell_x, markers_sell_y, '^', color="red")
    plt.plot(markers_buyShort_x, markers_buyShort_y, 'v', color="red")
    plt.plot(markers_sellShort_x, markers_sellShort_y, '^', color="green")
    plt.plot(markers_stop_x, markers_stop_y, 'x', color="black")
    tDayArrayX = arange(0.0, len(closeList), TIMEBASE)
    tDayArrayY = []
    for e in tDayArrayX:
        tDayArrayY.append(closeList[int(e)])
    plt.plot(tDayArrayX ,tDayArrayY , '|', color="black")
    #plt.xlim(0,2000)
    plt.show()


def buyLong(amount, price, fee, stop, index):
    global gAccountMoney
    global gAmountAssets
    global gStop

    money = amount*price*(1+(2*fee/100))
    if (money<=gAccountMoney):
        gAccountMoney = gAccountMoney - amount*price*(1+(fee/100))
        gAmountAssets = amount
        gStop = stop
        buyLongDict[index]=price

def sellLong(amount, price, fee, index):
    global gAccountMoney
    global gAmountAssets
    global gStop

    gAccountMoney = gAccountMoney + amount * price * (1 - (fee / 100))
    gAmountAssets = gAmountAssets - amount
    sellLongDict[index] = price

def sellShort(amount, price, fee, stop, index):
    global gAccountMoney
    global gAmountAssets
    global gStop

    money = amount*price*(1+(2*fee/100))
    if (money<=gAccountMoney):
        gAccountMoney = gAccountMoney + amount*price*(1-(fee/100))
        gAmountAssets = -amount
        gStop = stop
        sellShortDict[index]=price
        print ("go Short: " + str(price))

def buyShort(amount, price, fee, index):
    global gAccountMoney
    global gAmountAssets
    global gStop

    gAccountMoney = gAccountMoney + amount * price * (1 - (fee / 100))
    gAmountAssets = gAmountAssets + amount
    buyShortDict[index] = price
    print("exit Short: " + str(price))
    print ("profit (w/o fee): " + str(round((gEntryPrice/price-1)*100,2)) + "%")
    print ("Money: " + str(gAccountMoney))

#--------main--------
#---load Data---
l = utils.loadData("data")
closeList, highList, lowList = utils.fillLists(l)

#donchianHigh = utils.loadData("dhighFile"+str(DONCHIANDAYS*TIMEBASE))
#donchianLow  = utils.loadData("dlowFile"+str(DONCHIANDAYS*TIMEBASE))
#donchianHighStop = utils.loadData("dhighFile"+str(STOPDAYS*TIMEBASE))
#donchianLowStop  = utils.loadData("dlowFile"+str(STOPDAYS*TIMEBASE))

donchianHigh, donchianLow = utils.buildDonchian2(DONCHIANDAYS,TIMEBASE, highList, lowList)
donchianHighStop, donchianLowStop = utils.buildDonchian2(STOPDAYS,TIMEBASE, highList, lowList)
#donchianHigh, donchianLow = utils.buildDonchian(DONCHIANDAYS*TIMEBASE, highList, lowList)
#donchianHighStop, donchianLowStop = utils.buildDonchian(STOPDAYS*TIMEBASE, highList, lowList)
#utils.saveData("dhighFile"+str(DONCHIANDAYS*TIMEBASE),donchianHigh)
#utils.saveData("dlowFile"+str(DONCHIANDAYS*TIMEBASE),donchianLow)
#utils.saveData("dhighFile"+str(STOPDAYS*TIMEBASE),donchianHighStop)
#utils.saveData("dlowFile"+str(STOPDAYS*TIMEBASE),donchianLowStop)

#---buy and sell---
if 1:
    index = 0
    for price in closeList[:len(donchianHigh)]:
        if 0:
            #trailing Stop Long
            if (state == State.LONG):
                stop = utils.setStopLow(donchianLowStop, index, 1, TIMEBASE)
                gStop = stop = donchianLowStop[index-TIMEBASE]
                stopDict[int(index/TIMEBASE)*TIMEBASE] = stop

            #sellLong
            if ((state == State.LONG) and (price<gStop)):
                sellLong(gAmountAssets, price, FEE, index)
                state = State.EQUAL
            # buyLong
            if ((index > ((DONCHIANDAYS + 1) * TIMEBASE)) and (state == State.EQUAL)):
                if (utils.checkLong(price, donchianHigh, index, TIMEBASE)):
                    stop = donchianLowStop[index - TIMEBASE]
                    stopDict[int(index / TIMEBASE) * TIMEBASE] = stop
                    buyLong(AMOUNTOFCONTRACTS, price, FEE, stop, index)
                    print("INDEX LONG = " + str(index))
                    gEntryPrice = price
                    state = State.LONG

        if 1:
            #trailing Stop Short
            if (state == State.SHORT):
                stop = utils.setStopHigh(donchianHighStop, index, 1, TIMEBASE)
                gStop = stop = donchianHighStop[index-TIMEBASE]
                stopDict[int(index/TIMEBASE)*TIMEBASE] = stop

            # buyShort
            if ((state == State.SHORT) and (price > gStop)):
                buyShort(gAmountAssets, price, FEE, index)
                state = State.EQUAL

            # sellShort
            if ((index > ((DONCHIANDAYS + 1) * TIMEBASE)) and (state == State.EQUAL)):
                if (utils.checkShort(price, donchianLow, index, TIMEBASE)):
                    print ("--------------------")
                    stop = donchianHighStop[index - TIMEBASE]
                    stopDict[int(index / TIMEBASE) * TIMEBASE] = stop
                    sellShort(AMOUNTOFCONTRACTS, price, FEE, stop, index)
                    #print("INDEX SHORT = " + str(index))
                    gEntryPrice = price
                    state = State.SHORT
        index = index + 1


    profit = gAmountAssets*closeList[index]+gAccountMoney
    print ("Amount = "+ str(profit) + "("  + str(round((profit/STARTMONEY-1)*100,2)) + "%)")
    print("Assets = " + str(gAmountAssets))
    print("Money = " + str(gAccountMoney))
plotData()

#todo:
#Ausgabe Gewinn/Verlust und weitere Statistiken
