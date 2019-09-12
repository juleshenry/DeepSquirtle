import numpy as np 
import pandas as pd 

pdex = {}
with open('pokedex_dict.txt', 'r+') as f: exec('pdex = ' + f.read())

df = pd.read_csv('data.csv')