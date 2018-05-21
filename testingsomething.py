import numpy as np 
from pandas import DataFrame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import GetFromJson

#Pick the rooms and get indexes of it
test = GetFromJson.getMediaIndex('temperature', 'e22-601b-0')
test2 = GetFromJson.getMediaIndex('co2', 'e22-601b-0')

#Create dataframes of the rooms
df = GetFromJson.getDataframe(test)
df2 = GetFromJson.getDataframe(test2)

#Resample the dataframe into time intervals (specified i.e 2 hour) using the mean value
df = GetFromJson.getDataframeFreq(df, "1H")
df2 = GetFromJson.getDataframeFreq(df2, "1H")

#Remove outliers from the dataframes
df = GetFromJson.removeOutliersSD(df)
df2 = GetFromJson.removeOutliersSD(df2)

#Set the readings into specified intervals. Using min/max and wanted # of intervals
df = GetFromJson.setReadingIntervals(df, 7)
df2 = GetFromJson.setReadingIntervals(df2, 8)

#Get Boolean Association rules. Apriori
df = GetFromJson.getBooleanAssociationRules(df, df2)
df = GetFromJson.ap.apriori(df, 0.0000000001)

interval1 = 7
intervalsomething =8
interval2 = 8
combined = interval1+interval2
start = interval1+interval2+1
startinterval2 = start+interval2

Index= df['itemsets'][0:interval1].values
Cols = df['itemsets'][interval1:combined].values
a = [list(item) for item in df['itemsets'] ]
array = []
for i in range (interval1):
    for j in range (interval2):
        result = [df['itemsets'][i][0], df['itemsets'][interval2+j][0]]
        if result not in a:
            array.append([result, 0.0])

df2 = pd.DataFrame(array, columns=['itemsets', 'support'])
df = pd.concat([df, df2])
df = df.reset_index(drop=True)
df = df.loc[sorted(df.index, key=lambda i: (lambda t: (len(t), tuple(t)))(df.at[i, 'itemsets']))]

mylist = []
for i in range(interval1):
    mylist.append(df['support'][start:startinterval2].values)
    start = startinterval2
    startinterval2 = startinterval2+intervalsomething
print(mylist)
mat = np.array(mylist)

df = DataFrame((mat), index=Index, columns=Cols)
colormap = ["#63BE7B", "#91CB7D", "#FFE984", "#FED881", "#FCB279", "#FA8170", "#F8696B"]
sns.heatmap(df, annot=True, cmap=sns.color_palette(colormap))
plt.show()