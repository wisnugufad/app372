from math import floor, sqrt
import pandas as pd
import numpy as np

def calculate(alpha, beta, flower):
    xls = pd.read_excel('db.xlsx')

    df = xls[flower]

    length = len(df)

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

    index = 0
    while index < length:
        if index > 1:
            cL = alpha * df[index] + (1 - alpha) * (level[index-1] + trend[index-1])
            level.append(cL)

            cT = beta * (level[index] - level[index-1]) + (1 - beta) * trend[index-1]
            trend.append(cT)

            forecast.append(level[index-1] + trend[index-1])
            tempForecast.append(level[index-1] + trend[index-1])

            error.append(df[index] - forecast[index])

            absErrorPower.append(pow(error[index],2))

            mad.append(np.absolute(error[index]))

            mape.append(round(mad[index]/df[index]*100))

        data.append(df[index])
        tempData.append(df[index])
        index += 1
    
    resForecast.append(level[length-1] + trend[length-1])
    tempForecast.append(level[length-1] + trend[length-1])
    tempData.append(data[len(data)-1])
    
    
    i = 1
    while i < 4:
        resForecast.append(trend[length-1] + resForecast[i-1])
        tempForecast.append(trend[length-1] + resForecast[i-1])
        tempData.append(data[len(data)-1])
        i += 1

    j = 0
    lengthError = len(absErrorPower)
    while j < lengthError:
        rsme = rsme + absErrorPower[j]
        j += 1
    
    rsme = sqrt(rsme / lengthError)
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

    return result