import numpy as np
import pandas as pd

def generate_new_combinations(old_combinations):
    items_types_in_previous_step = np.unique(old_combinations.flatten())
    for old_combination in old_combinations:
        max_combination = max(old_combination)
        for item in items_types_in_previous_step:
            if item > max_combination:
                res = tuple(old_combination) + (item,)
                yield res

#Apriori algorithm calculating the support of the itemsets
def apriori(df, min_support):
    X = df.values
    ary_col_idx = np.arange(X.shape[1])
    support = (np.sum(X, axis=0) / float(X.shape[0]))
    support_dict = {1: support[support >= min_support]}
    itemset_dict = {1: ary_col_idx[support >= min_support].reshape(-1, 1)}
    max_itemset = 1

    while max_itemset:
        next_max_itemset = max_itemset + 1
        combin = generate_new_combinations(itemset_dict[max_itemset])
        frequent_items = []
        frequent_items_support = []

        for c in combin:
            together = X[:, c].all(axis=1)
            support = together.sum() / len(X)
            if support >= min_support:
                frequent_items.append(c)
                frequent_items_support.append(support)

        if frequent_items:
            itemset_dict[next_max_itemset] = np.array(frequent_items)
            support_dict[next_max_itemset] = np.array(frequent_items_support)
            max_itemset = next_max_itemset
        else:
            max_itemset = 0
  
    all_res = []
    for k in sorted(itemset_dict):
        support = pd.Series(support_dict[k])
        itemsets = pd.Series([i for i in itemset_dict[k]])

        result = pd.concat((support, itemsets), axis=1)
        all_res.append(result)

    supportDf = pd.concat(all_res)
    supportDf.columns = ['support', 'itemsets']
    supportDf = supportDf.reset_index(drop=True)
    
    return supportDf   

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