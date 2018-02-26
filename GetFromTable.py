

import MySQLdb, matplotlib.pyplot as plt



database = MySQLdb.connect( host = "localhost", user = "root", passwd = "", db = "bachelor")
cursor = database.cursor()



query = """SELECT Sensortype, TimeInMiliseconds, Reading, Room FROM data WHERE data.TimeInMiliseconds and data.SensorType = 'air' and data.Room = 'e22-601b-0'"""


cursor.execute(query)
databaseTuple = cursor.fetchall()


cursor.close()

time =[]
reading = []

database.commit()


def getTupleColumn(index, list):
    for i in range(len(databaseTuple)):
        list.append(databaseTuple[i][index])

def milisecondsToSeconds(list):
    for i in range(len(list)):
        list[i] = list[i]/1000

getTupleColumn(1,time)
getTupleColumn(2,reading)
milisecondsToSeconds(time)

plt.scatter(time, reading)
plt.show()
print (databaseTuple[0])
print (len(time))
print (time[0])