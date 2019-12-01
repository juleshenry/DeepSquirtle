import numpy as np 
import pandas as pd
from DataTransformer import *
from DataNormalizer import *

class DataManager:
    def __init__(self, dmdf):
        self.dmdf = self.preprocess(dmdf, 1400, 5)
        self.transformer = DataTransformer()
        self.normalizer = DataNormalizer()

    def preprocess(self, dmdf, elo, turns):
        dmdf.sort_values('elo', ascending=False)
        dmdf = dmdf.drop_duplicates(subset = 'battle_url', keep='first')
        dmdf = dmdf.drop(['battle_url'], axis=1)
        dmdf = dmdf.dropna()
        dmdf = dmdf[dmdf.elo != 2019]
        dmdf = dmdf[dmdf.elo >= elo]
        dmdf = dmdf[dmdf.num_turns > 5] #TODO: could be deviation from mean turns
        return dmdf

    #forgot how to remove duplicates by a repeated column....
    def duplicate_remove(self, data):
        return data

    def create_analytics_base_table(self):
        return self.normalizer.normalize(self.transformer.transform(self.dmdf))

data = pd.read_csv('data.csv')
dm = DataManager(data).create_analytics_base_table()