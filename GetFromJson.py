import pandas as pd
#from scipy import stats
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
    df = df.set_index('timestamp')
    return df

#Get a specified time frequency of the dataframe i.e '45Min'
def getDataframeFreq(df, freq):
    df = df.resample(freq)['readings'].mean()
    df = df.dropna()
    df = df.to_frame()
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
def setReadingIntervals(df, intervals):
    bins = []
    labels = []
    bins.append(df.min())

    incrementValue = (df.max()-df.min())/intervals
    bins = np.arange(df.min()-1,df.max()+1+incrementValue/intervals,incrementValue)

    for i in range(0, len(bins)-1):
        label = "{0:.1f}".format(bins[i]) +'-'+"{0:.1f}".format(bins[i+1])
        labels.append(label)
    df['readings'] = pd.cut(df['readings'], bins=bins, labels=labels)
    return df

#Return a dataframe with boolean assocation rules
def getBooleanAssociationRules(df, df2):
    df = df.merge(df2, left_index=True, right_index=True, how='inner')
    df = pd.get_dummies(df)
    return df

#Set interpolation
def createInterpolation(df, interval):
    df = df.resample(interval)['readings'].mean()
    df = df.dropna()
    df = df.to_frame()
    timerange = pd.date_range(df.index[0], df.index[-1], freq=interval)
    dfWithIntervals = timerange.union(df.index)
    dfWithIntervals = df.reindex(dfWithIntervals)
    dfWithIntervals = dfWithIntervals.interpolate(method="time")
    return dfWithIntervals

#Remove outliers
def removeOutliersSD(df):
    df = df[df.apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1)]
    return df

def removeOutliersIQR(df):
    Q1 = df['readings'].quantile(0.25)
    Q3 = df['readings'].quantile(0.75)
    IQR = (df['readings'] > Q1) & (df['readings'] < Q3)
    return df.loc[IQR]

def dataframeFromTime(df, fromtime, totime):
    df = df[df.index > pd.to_datetime(fromtime, unit='ms')]
    df = df[df.index < pd.to_datetime(totime, unit='ms')]
    return df

#Pick the rooms and get indexes of it
test = getMediaIndex('temperature', 'e22-601b-0')
test2 = getMediaIndex('co2', 'e22-601b-0')

#Create dataframes of the rooms
df = getDataframe(test)
df2 = getDataframe(test2)

#Resample the dataframe into time intervals (specified i.e 2 hour) using the mean value
#df = getDataframeFreq(df, "2H")
#df2 = getDataframeFreq(df2, "2H")

#Create interpolating data every specified interval. Uses time interpolation
df = createInterpolation(df, '30Min')
df2 = createInterpolation(df2, '30Min')

#Remove outliers from the dataframes
df = removeOutliersSD(df)
df2 = removeOutliersSD(df2)



#Set the readings into specified intervals. Using min/max and wanted # of intervals
df = setReadingIntervals(df, 2)
df2 = setReadingIntervals(df2, 15)

#Get Boolean Association rules. Apriori
df = getBooleanAssociationRules(df, df2)
df = ap.apriori(df, 0.1)

#Using the apriori dataframe, confidence, lift etc can be calculated
#ap.allConfidence(df,0.1)
#print(ap.allLift(df, 0.1))
