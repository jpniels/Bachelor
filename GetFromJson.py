import pandas as pd
import json

#Read JSON file from path
def read_file_path(path):
    with open(path, 'r'):
        data = pd.read_json(path)
    return data

data = read_file_path('ou44_gnd.json')

#Get a dataframe with timeintervals and mean readings for those
def getDataframe():
    readings = getReadings()
    time = getTime()
    df = pd.DataFrame({'timestamp':time.values, 'readings':readings.values})
    df = df.groupby(pd.Grouper(key='timestamp', freq='12H'))['readings'].mean()
    df = df.dropna()
    return df

#Get all the rooms from the data
def getRooms():
    roomnames = []
    for i in range(0, len(data)):
        room = data['Metadata'][i]['Location']['Room']
        if room not in roomnames:
            roomnames.append(room)
    return roomnames

#Return the readings of the data
def getReadings():
    readings = data.Readings[2]
    measurement = pd.Series(i[1] for i in readings)
    return measurement

#Return time of the readings
def getTime():
    time = data.Readings[2]
    time = pd.Series(i[0] for i in time)
    time = pd.to_datetime(time, unit='ms')
    return time

#Return dataframe with time and reading intervals
def setReadingIntervals():
    df = getDataframe()
    df = pd.cut(df, bins=[17,18,19,20,21,22,23,24,25,26,27,28], labels=['17-18','18-19','19-20','20-21','21-22','22-23','23-24','24-25','25-26','26-27','27-28'])
    return df

def getBooleanAssociationRules():
    df = setReadingIntervals()
    df = pd.get_dummies(df)
    return df

#Set interpolation
def createInterpolation(interval):
    df = getDataframe()
    timerange = pd.date_range(df.index[0], df.index[-1], freq=interval, normalize=True)

    dfWithIntervals = timerange.union(df.index)
    dfWithIntervals = df.reindex(dfWithIntervals)
    dfWithIntervals = dfWithIntervals.interpolate(method="time")
    return dfWithIntervals