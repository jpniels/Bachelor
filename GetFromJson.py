import pandas as pd



def read_file_path(path):
    with open(path, 'r'):
            objects  = pd.read_json(path)
            return objects

data = read_file_path('ou44_gnd.json')
#data['TimeInMiliseconds'] = pd.to_datetime(data['TimeInMiliseconds'], unit='ms')
data = data.rename(columns={'TimeInMiliseconds': 'Date'})
print(data)

def getReadings():
    readings = data.where(data.Unit == 'degree celcius')
    return readings.Reading

def getTime():
    time = data.where(data.Unit == 'degree celcius')
    return time.Date  