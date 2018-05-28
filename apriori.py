import numpy as np
import pandas as pd

#Look for new combinations
def newCombinations(oldCombos):
    previousStep = np.unique(oldCombos.flatten())
    for oldCombi in oldCombos:
        maxCombi = max(oldCombi)
        for value in previousStep:
            if value > maxCombi:
                res = tuple(oldCombi) + (value,)
                yield res

#Apriori algorithm calculating the support of the itemsets
def apriori(df, minSupport):
    values = df.values
    index = np.arange(values.shape[1])
    support = (np.sum(values, axis=0) / float(values.shape[0]))
    supportDict = {1: support[support >= minSupport]}
    valuesetDict = {1: index[support >= minSupport].reshape(-1, 1)}
    maxValueset = 1

    while maxValueset:
        newMaxValueset = maxValueset + 1
        combin = newCombinations(valuesetDict[maxValueset])
        frequentValues = []
        frequentValuesSupport = []

        for c in combin:
            combined = values[:, c].all(axis=1)
            support = combined.sum() / len(values)
            if support >= minSupport:
                frequentValues.append(c)
                frequentValuesSupport.append(support)

        if frequentValues:
            valuesetDict[newMaxValueset] = np.array(frequentValues)
            supportDict[newMaxValueset] = np.array(frequentValuesSupport)
            maxValueset = newMaxValueset
        else:
            maxValueset = 0
  
    resultsDataFrame = concatSets(supportDict, valuesetDict)
    return resultsDataFrame 

#Concat the support and valueset into dataframe
def concatSets(supportSet,valueSet):
    allResults = []
    for k in sorted(valueSet):
        support = pd.Series(supportSet[k])
        valuesets = pd.Series([i for i in valueSet[k]])

        result = pd.concat((support, valuesets), axis=1)
        allResults.append(result)

    supportDf = pd.concat(allResults)
    supportDf.columns = ['support', 'itemsets']
    supportDf = supportDf.reset_index(drop=True)
    
    return supportDf   

#Calculate the confidence for all values
def allConfidence(df, min_confidence):
    print(df)
    df2 = df.loc[df['itemsets'].str.len() > 1] #df with 2 values
    df3 = df.loc[df['itemsets'].str.len() <= 1] #df with less than 2 values

    #empty arrays for filling up
    ante = []
    conse = []      
    conf = []
    
    for index, row in df2.iterrows(): #going through each element that contains 2 values
        for index, row2 in df3.iterrows(): #go though each element that contains less than 2 values
            if (row['itemsets']==row2['itemsets']).any() == True: #check if a value is a part of the other
                confvalue = row['support']/row2['support'] #calculate confidence
                if confvalue >= min_confidence: #fill arrays if confidence is above min_confidence
                    ante.append(row2['itemsets'])
                    conse.append(row['itemsets'])
                    conf.append(confvalue)
    confDf = pd.DataFrame(list(zip(ante, conse, conf)),columns=['antecedants','consequents', 'confidence']) #create dataframe with values
    print(confDf)
    return confDf

#Calculate the lift for all values
def allLift(df, min_lift):
    df2 = df.loc[df['itemsets'].str.len() > 1]
    df3 = df.loc[df['itemsets'].str.len() <= 1]

    #empty arrays for filling up
    ante = []
    conse = []
    lift = []
    
    for index, row in df2.iterrows():
        for index, row2 in df3.iterrows(): 
            if (row['itemsets']==row2['itemsets']).any() == True: 
                for index, row3 in df3.iterrows(): 
                    testingvalue = np.append(row2['itemsets'], (row3['itemsets']))
                    if(np.sort(testingvalue) == row['itemsets']).all() == True:
                        liftvalue =  row['support']/(row2['support']*row3['support'])
                        if liftvalue >= min_lift: 
                            ante.append(row2['itemsets'])
                            conse.append(row3['itemsets'])
                            lift.append(liftvalue)
    liftDf = pd.DataFrame(list(zip(ante, conse, lift)),columns=['antecedants','consequents', 'lift'])
    return liftDf

#Calculate the conviction for all calues
def allConviction(supp, conf):
    conviction = []
    tempConf = conf
    for i in range(0,len(supp)):
        for j in range(0, len(supp['itemsets'][i])):
            for ii in range(0, len(conf)):
                for jj in range(0, len(conf['consequents'][ii])):
                    if supp['itemsets'][i][j] != conf['antecedants'][ii][0] and len(supp['itemsets'][i]) <=1:
                        if supp['itemsets'][i][j] == conf['consequents'][ii][jj]:
                            conviction.append((1-supp['support'][i])/(1-conf['confidence'][ii]))
                            conf.drop([ii])
                            supp.drop([i])
    tempConf['conviction'] = conviction                      
    return tempConf