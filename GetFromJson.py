import pandas as pd
import json

#Read JSON file from path
def read_file_path(path):
    with open(path, 'r'):
            objects = pd.read_json(path)
            return objects

data = read_file_path('ou44_gnd.json')

#Return the readings
def getReadings():
    readings = data.Readings[2]
    measurement = pd.Series(i[1] for i in readings)
    return measurement

#Return time of the readings
def getTime():
    readings = data.Readings[2]
    time = pd.Series(i[0] for i in readings)
    time = pd.to_datetime(time, unit='ms')
    return time