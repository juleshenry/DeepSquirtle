from DataTransformer import *
from DataNormalizer import *

class DataManager:
    def __init__(self, data):
        self.data = data
        self.transformer = DataTransformer()
        self.normalizer = DataNormalizer()

    def create_analytics_base_table(self):
        return = self.normalizer.normalize(self.transformer.transform(self.data))
