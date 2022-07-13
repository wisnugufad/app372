from math import floor, sqrt
import pandas as pd
import numpy as np

def calculate(alpha, beta, flower):
    # import data db.xlsx to variable
    xls = pd.read_excel('db.xlsx')

    # get data flower into variable
    df = xls[flower]

    # count data flower
    length = len(df)

    # declare and inisiate variable
    data = []
    level = [0, df[1]]
    trend = [0, df[1] - df[0]]
    forecast = [0,0]
    error = [0,0]
    absErrorPower = []
    mad = [0,0]
    mape = [0,0]

    tempData = []
    tempForecast = [0,0]
    resForecast = []

    rsme = 0.00

    # declare index as 0 for begining
    index = 0
    # loop as much as length data
    while index < length:
        # conditional data if index less then 1 so it not do a calculate
        if index > 1:
            # t as Time as index or looping index
            # cL mean counting level
            # cl = alpha * data[t] + (1 - alpha) * (level[t-1] + trend[t-1])
            cL = alpha * df[index] + (1 - alpha) * (level[index-1] + trend[index-1])
            # insert cL value into level
            level.append(cL)

            # cT mean counting trend
            # cT = beta * (level[t] - level[t-1]) + (1 - beta) * trend[t-1]
            cT = beta * (level[index] - level[index-1]) + (1 - beta) * trend[index-1]
            # insert cT value into trend
            trend.append(cT)

            # do a forecast 
            # ft = level[t-1] + trend[t-1] then insert into it and tempForecast
            forecast.append(level[index-1] + trend[index-1])
            tempForecast.append(level[index-1] + trend[index-1])

            # do calculate error
            # error = data[t] - ft[t] then insert into it
            error.append(df[index] - forecast[index])

            # |error|^2
            absErrorPower.append(pow(error[index],2))

            # insert abs error into MAD
            mad.append(np.absolute(error[index]))

            # calculate percentage error
            # rounding MAD[t] / data[t] * 100%
            mape.append(round(mad[index]/df[index]*100))

        # insert data flower[t] into data variable and temp
        data.append(df[index])
        tempData.append(df[index])

        # loop/index + 1
        index += 1
    
    # resForecast mean rest of forecast what we will predict
    # for index 0 or first index forecast will be initiate
    # rF = level[last index] + trend[last index]
    resForecast.append(level[length-1] + trend[length-1])
    tempForecast.append(level[length-1] + trend[length-1])

    # temp data we insert as much as res forecast so if we add 1 more forecast we must add 1 more in temp data
    tempData.append(data[len(data)-1])
    
    # index start from zero, because we insert first index previously we start index from 1
    i = 1
    # why 4 ? because we want predict 4 weeks / 4 times
    while i < 4:
        # t as Time as index or looping i
        # rF = trend[last index] + rF[t-1]
        resForecast.append(trend[length-1] + resForecast[i-1])
        tempForecast.append(trend[length-1] + resForecast[i-1])
        # as we declare previously if we add 1 forecast we must add 1 more in temp data
        tempData.append(data[len(data)-1])
        # loop/i + 1
        i += 1

    # so why now zero ? because we calculate all absErrorPower so we add from start
    j = 0
    # length of absErrorPower
    lengthError = len(absErrorPower)
    while j < lengthError:
        # rsme = rsme + absErrorPower[t]
        rsme = rsme + absErrorPower[j]
        # loop/j + 1
        j += 1
    
    # do a square root of rsme / length of absErrorPower
    rsme = sqrt(rsme / lengthError)

    # initiate object to main so we declare an object with value we calculate
    d = { 
            'flower': data,
            'level': level,
            'trend': trend,
            'forecast': forecast,
            'error': error,
            'MAD': mad,
            'MAPE': mape
        }
    
    q = {
        'flower': tempData,
        'forecast': tempForecast
    }

    result = {
        'table': d,
        'forecast': {
            'forecast': resForecast
        },
        'chart': q,
        'rsme': rsme
    }

    # return data to main
    return result