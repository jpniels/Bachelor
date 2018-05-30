import unittest
import sys
import gui
import GetFromJson
import apriori
import pandas as pd
import numpy as np
import numpy.testing as npt
from gui import mainWindow
from time import sleep
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        #Create dataframes for testing
        df = pd.DataFrame({'readings': [20,21, 20, 21, 22, 21, 24, 24, 22, 21], 'timestamp':[pd.to_datetime('2017-04-01'),
                                        pd.to_datetime('2017-04-02'), pd.to_datetime('2017-04-03'),pd.to_datetime('2017-04-04'),
                                        pd.to_datetime('2017-04-05'),pd.to_datetime('2017-04-06'),pd.to_datetime('2017-04-07'),
                                        pd.to_datetime('2017-04-08'),pd.to_datetime('2017-04-09'),pd.to_datetime('2017-04-10')]})    
        df = df.set_index('timestamp')
        df = GetFromJson.setReadingIntervals(df, 5)

        df2 = pd.DataFrame({'readings': [250, 400, 330, 400, 290, 500, 700, 600, 300, 275], 'timestamp':[pd.to_datetime('2017-04-01'),
                                        pd.to_datetime('2017-04-02'), pd.to_datetime('2017-04-03'),pd.to_datetime('2017-04-04'),
                                        pd.to_datetime('2017-04-05'),pd.to_datetime('2017-04-06'),pd.to_datetime('2017-04-07'),
                                        pd.to_datetime('2017-04-08'),pd.to_datetime('2017-04-09'),pd.to_datetime('2017-04-10')]})   
        df2 = df2.set_index('timestamp')
        df2 = GetFromJson.setReadingIntervals(df2, 5)

        self.df = GetFromJson.getBooleanAssociationRules(df, df2)

    def testSupport(self):
        df = apriori.apriori(self.df, 0.00001)
        npt.assert_array_equal(df.iloc[8][0], [0.2])

    def testConfidence(self):
        df = apriori.apriori(self.df, 0.00001)
        df = apriori.allConfidence(df, 0)
        npt.assert_array_equal(df.iloc[0][2], [1.0])

    def testLift(self):
        df = apriori.apriori(self.df, 0.00001)
        df = apriori.allLift(df, 0)
        npt.assert_array_equal(df.iloc[0][2], [2.0])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)