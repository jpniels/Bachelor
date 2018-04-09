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

        res = pd.concat((support, itemsets), axis=1)
        all_res.append(res)

    res_df = pd.concat(all_res)
    res_df.columns = ['support', 'itemsets']
    res_df = res_df.reset_index(drop=True)
    
    return res_df   

def allConfidence(df, threshold):
    df2 = df.loc[df['itemsets'].str.len() > 1] #create dataframe which contains all values with 2
    df3 = df.loc[df['itemsets'].str.len() <= 1]
    ante = []
    conse = []
    conf = []
    for index, row in df2.iterrows(): #going through each element that contains 2 values
        for index, row2 in df3.iterrows():
            if (row['itemsets']==row2['itemsets']).any() == True:
                confvalue = row['support']/row2['support']
                if confvalue >= threshold:
                    ante.append(row2['itemsets'])
                    conse.append(row['itemsets'])
                    conf.append(confvalue)
    confDf = pd.DataFrame(list(zip(ante, conse, conf)),columns=['antecedants','consequents', 'confidence'])
    return confDf


# def allConfidence(df, threshold):     
#     conf = pd.DataFrame({'confidence':[],'rule':[]})
#     upperMask = df.loc[df['itemsets'].str.len() >1]
#     lowerMask = df.loc[df['itemsets'].str.len() <=1]
#     for i in range (0, len(lowerMask)):
#         valueLMask = lowerMask.get_value(i,'support')
#         ruleLMask = lowerMask.get_value(i,'itemsets')
#         for j in range(7, len(upperMask)+6):
#             valueUMask = upperMask.get_value(j,'support')
#             ruleUMask = upperMask.get_value(j,'itemsets')
#             print(type(ruleUMask))
#             if((ruleLMask==ruleUMask).any() == True):
#                 if(valueUMask/valueLMask > threshold):
#                     tempList = str(ruleLMask) + ',' + str(ruleUMask)
#                     tempConf = pd.DataFrame({'confidence':[valueLMask/valueUMask],'rule':[tempList]})
#                     conf.append(tempConf)
#     return conf

# def allLift(df):


# def confidence(X, Y):
#     support(X and Y)/support(X)

# def lift(X, Y):
#     support(X and Y)/(support(X)*support(Y))