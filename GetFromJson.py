import pandas as pd
import json



def read_file_path(path):
    with open(path, 'r'):
            objects = pd.read_json(path)
            return objects

data = read_file_path('ou44_gnd.json')
#data['TimeInMiliseconds'] = pd.to_datetime(data['TimeInMiliseconds'], unit='ms')
#data = data.rename(columns={'TimeInMiliseconds': 'Date'})



def getReadings():
    time = []
    measurement = []
    readings = data.Readings[2]
    print(len(readings))
    for i in range(0, len(readings)):
        time.append( readings[i][0])
        measurement.append(readings[i][1])

    return time, measurement
print(getReadings())
def getTime():
    time = data.where(data.Unit == 'degree celcius')
    return time.Date  