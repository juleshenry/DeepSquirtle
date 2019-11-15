import numpy as np
import pandas as pd
from DataTransformer import *
from DataNormalizer import *

class DataManager:
    def __init__(self, dmdf):
        self.dmdf = dmdf
        self.transformer = DataTransformer()
        self.normalizer = DataNormalizer()

    def preprocess(self, turns):
        self.dmdf = self.dmdf.drop(['battle_url'],axis=1)
        self.dmdf = self.dmdf.dropna()
        self.dmdf = self.dmdf[self.dmdf.num_turns > 5] #TODO: could be deviation from mean turns

    def create_analytics_base_table(self):
        return self.normalizer.normalize(self.transformer.transform(self.dmdf))

data = pd.read_csv('data.csv')
dm = DataManager(data)
