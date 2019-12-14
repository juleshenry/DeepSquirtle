import pandas as pd
import numpy as np

class DataNormalizer:
    def normalize(self, data):
        data['highest_speed_flag'] = data['highest_speed_flag'].astype('category').cat.codes
        data['result'] = data['result'].astype('category').cat.codes

        for col in data.columns.tolist():
            print(col,data[col].dtype)
            if data[col].dtype == np.float64:
                maxi = data[col].max()
                mini = data[col].min()
                data[col] = data[col].apply(lambda row: (row - mini)/(maxi - mini))
                
        return data

    def normalize_one_way(self, data):
        pass

    def normalize_another_way(self, data):
        pass

    def utility_function_1(self, arg):
        pass

    def utility_function_2(self, arg):
        pass
