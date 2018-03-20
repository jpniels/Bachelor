import pandas as pd
import json

#Read JSON file from path
def read_file_path(path):
    with open(path, 'r'):
        data = pd.read_json(path)
    return data

data = read_file_path('ou44_gnd.json')

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
def setIntervals():
    readings = getReadings()
    time = getTime()
    df = pd.DataFrame({'timestamp':time.values, 'readings':readings.values})
    df = df.groupby(pd.Grouper(key='timestamp', freq='12H'))['readings'].mean()
    print(df.describe())
    v = pd.cut(df, bins=[17,18,19,20,21,22,23,24,25,26,27,28], labels=['17-18','18-19','19-20','20-21','21-22','22-23','23-24','24-25','25-26','26-27','27-28'])
    print (pd.get_dummies(v))
    return df
setIntervals()