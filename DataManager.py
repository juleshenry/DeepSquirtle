
import inspect
import numpy as np
import pandas as pd
from DataTransformer import *
from DataNormalizer import *

# Consumes a dataframe with the following header: battle_url, team_1, team_2, num_turns, result, elo, p1_elo, p2_elo, disconnect
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
        elo_valid_slice = dmdf['elo'] != 2019
        elo_avg = elo_valid_slice.mean()
        dmdf['elo'] = np.where(dmdf['elo'] == 2019, elo_avg, dmdf['elo'])
        dmdf = dmdf[dmdf.elo >= elo]
        dmdf = dmdf[dmdf.num_turns > 5]
        return dmdf


    def create_analytics_base_table(self):
        return self.normalizer.normalize(self.transformer.transform_from_class_dict(self.dmdf))

if __name__ == "__main__":
    data = pd.read_csv('battle_data.csv')
    dm = DataManager(data).create_analytics_base_table()

    # dt = DataTransformer()
    # a = [func for func in dir(dt) if callable(getattr(dt, func)) and not func.startswith("__")]
    # b = [str(inspect.signature(getattr(dt, func))) for func in dir(dt) if callable(getattr(dt, func)) and not func.startswith("__")]
    # c = [type(getattr(dt, func)) for func in dir(dt) if callable(getattr(dt, func)) and not func.startswith("__")]
    # for i in b:
    #     if 'stat' in i:
    #         print('statbased:',i)
    #     else:
    #         print([arg.replace('(','').replace(')','').replace(' ','') for arg in i.split(',')])
