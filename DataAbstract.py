import numpy as np 
import pandas as pd 

def destring(s):
    #if s[0]== '[' and s[-1] == ']'
    return s.replace("[",'').replace(']','').replace("'",'').replace(' ','').split(",")

def pokekey(s): return s.lower().replace('-','')