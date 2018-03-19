import MySQLdb, matplotlib.pyplot as plt, matplotlib.dates as mdate

#connect to database
database = MySQLdb.connect( host = "localhost", user = "root", passwd = "", db = "bachelor")
cursor = database.cursor()

#gets the degrees celcius from room e22-601b-0
def getDegrees(room):
    query = """SELECT Sensortype, TimeInMiliseconds, Reading, Room
           FROM data WHERE TimeInMiliSeconds
           and data.SensorType = 'air'
           and data.Room = """+ room + """
           and data.Unit = 'degree celcius'"""
    return query

#Gets the CO2 of  room e22-601b-0
def getCO2(room):
    query = """SELECT Sensortype, TimeInMiliSeconds, Reading, Room
      FROM data WHERE TimeInMiliSeconds
      and data.Sensortype = 'air'
      and data.Room = """+ room +""" 
      and data.Unit = 'parts per million'"""
    return query


cursor.execute(getDegrees("'e22-601b-0'"))
databaseTuple = cursor.fetchall()


cursor.close()

timeCO2 = []
readingCO2 = []


timeDegrees =[]
readingDegrees = []

database.commit()

#this function removes 0's from the data set to give a better picture of the code
#it takes 2 lists, 1 with the reading and the one you want to remove the 0's from
def removeZero(readingDegrees, listToRemoveFrom):
    newList = []

    for i in range(len(readingDegrees)):
        if (readingDegrees[i] > 1):
            newList.append(listToRemoveFrom[i])

    return newList
#gets the coulmn of the tuple inserted.
#you have to know at which index the data you want is
def getTupleColumn(index, list):
    for i in range(len(databaseTuple)):
        list.append(databaseTuple[i][index])

#converts milliseonds to seconds
def milisecondsToSeconds(list):
    for i in range(len(list)):
        list[i] = list[i]/1000

#gets the touples and converts to seconds
getTupleColumn(1,timeDegrees)
getTupleColumn(2,readingDegrees)
milisecondsToSeconds(timeDegrees)

secs = mdate.epoch2num(timeDegrees)


print (type(timeDegrees))
fig, ax = plt.subplots()



#change to dates and setting the plot
date_fmt = '%d-%m-%y %H:%M:%S'
date_formatter = mdate.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)
fig.autofmt_xdate()

"""
Here we can show if we outcomment the code, the "errors" which are in the data
"""
#ax.plot_date(secs, readingDegrees)
#plt.show()




#setting the new lists without 0's
readingDegrees = removeZero(readingDegrees,readingDegrees)
timeDegrees = removeZero(readingDegrees,timeDegrees)

#changing for use to plot
secs = mdate.epoch2num(timeDegrees)
ax.plot_date(secs, readingDegrees)
plt.show()


print (databaseTuple[0])
print (len(timeDegrees))
print (timeDegrees[0])

cursor = database.cursor()

cursor.execute(getCO2("'e22-601b-0'"))
databaseTuple = cursor.fetchall()


cursor.close()

database.commit()

getTupleColumn(1,timeCO2)
getTupleColumn(2,readingCO2)
milisecondsToSeconds(timeCO2)

secs = mdate.epoch2num(timeCO2)


print (type(timeDegrees))
fig, ax = plt.subplots()



#change to dates and setting the plot
date_fmt = '%d-%m-%y %H:%M:%S'
date_formatter = mdate.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)
fig.autofmt_xdate()
ax.plot_date(secs, readingCO2)
plt.show()