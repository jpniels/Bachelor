import numpy as np
import pandas as pd

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

def concatSets(supportSet,valueSet):
    allResults = []
    for k in sorted(valueSet):
        support = pd.Series(supportSet[k])
        valuesets = pd.Series([i for i in valueSet[k]])

<<<<<<< HEAD
        result = pd.concat((support, valuesets), axis=1)
        allResults.append(result)

    resdf = pd.concat(allResults)
    resdf.columns = ['support', 'itemsets']
    resdf = resdf.reset_index(drop=True)
    
    return resdf
    
=======
        result = pd.concat((support, itemsets), axis=1)
        all_res.append(result)

    supportDf = pd.concat(all_res)
    supportDf.columns = ['support', 'itemsets']
    supportDf = supportDf.reset_index(drop=True)
    
    return supportDf   
>>>>>>> df826fd80ef1b2dcb338ac1af55e84448f712645

#Calculate the confidence for all values
def allConfidence(df, min_confidence):
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
    return confDf

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

# def confidence(ante, conse):
#     create dataframe from the 2 values
#     allConfidence(newDf)
#     support(X and Y)/support(X)

# def lift(ante, conse):
#     support(X and Y)/(support(X)*support(Y))