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
        if (i%1000 == 0):
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