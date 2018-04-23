import pandas as pd
from scipy import stats
import numpy as np
import apriori as ap

#Read JSON file from path
def read_file_path(path):
    with open(path, 'r'):
        data = pd.read_json(path)
    return data

data = read_file_path('assets/ou44_gnd.json')

#Get a dataframe with timeintervals and mean readings
def getDataframe(index):
    readings = pd.Series()
    time = pd.Series()
    for i in range( 0, len(index)):
        readings = readings.append(getReadings(index[i]))
        time = time.append(getTime(index[i]))
    df = pd.DataFrame({'timestamp':time.values, 'readings':readings.values})
    df = df.sort_values(by=['timestamp'])
    return df

#Get a specified time frequency of the dataframe i.e '45Min'
def getDataframeFreq(df, freq):
    df = df.groupby(pd.Grouper(key='timestamp', freq=freq))['readings'].mean()
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

#Return a dictionary of a specified room i.e 'e21-602-0'
def getMedias(room):
    medias = {}
    for i in range(0, len(data)):
        if room == data['Metadata'][i]['Location']['Room']:
            medias[i] = data['Metadata'][i]['Modality']
    return medias

#Return the index of a specified media i.e 'temperature'
def getMediaIndex(modality, room):
    medias = getMedias(room)
    keys = []
    for key, val in medias.items():
        if modality == val:
            keys.append(key)
    return keys

#Return the readings of the data
def getReadings(index):
    readings = data.Readings[index]
    measurement = pd.Series(i[1] for i in readings)
    return measurement

#Return time of the readings
def getTime(index):
    time = data.Readings[index]
    time = pd.Series(i[0] for i in time)
    time = pd.to_datetime(time, unit='ms')
    return time

#Return dataframe with time and reading intervals
def setReadingIntervals(df):
    df = pd.cut(df, bins=[10,18,19,20,21,22,23,24,25,26,27,28, 300, 400, 500, 600, 700, 1500], labels=['10-18','18-19','19-20','20-21','21-22','22-23','23-24','24-25','25-26','26-27','27-28', '28-300', '300-400', '400-500', '500-600', '600-700', '700-1500'])
    return df 

#Return a dataframe with boolean assocation rules
def getBooleanAssociationRules(co2, temp):
    co2 = co2.to_frame()
    temp = temp.to_frame()
    df = co2.merge(temp, left_index=True, right_index=True, how='inner')
    df = pd.get_dummies(df)
    return df

#Set interpolation
def createInterpolation(df, interval):
    timerange = pd.date_range(df.index[0], df.index[-1], freq=interval, normalize=True)
    dfWithIntervals = timerange.union(df.index)
    dfWithIntervals = df.reindex(dfWithIntervals)
    dfWithIntervals = dfWithIntervals.interpolate(method="time")
    return dfWithIntervals

#Detect outliers using IQR
def removeOutliers(df):
    df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
    return df

test = getMediaIndex('temperature', 'e22-601b-0')
test2 = getMediaIndex('co2', 'e22-601b-0')
df = getDataframe(test)
df2 = getDataframe(test2)
print(df)
#df = removeOutliers(df)
#df2 = removeOutliers(df2)
df = getDataframeFreq(df, "2H")
df2 = getDataframeFreq(df2, "2H")
df = setReadingIntervals(df)
df2 = setReadingIntervals(df2)
df = getBooleanAssociationRules(df, df2)
df = ap.apriori(df, 0.1) 
print(ap.allConfidence(df,0.1))