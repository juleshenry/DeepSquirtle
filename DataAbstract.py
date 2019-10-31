import numpy as np
import pandas as pd

def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func

def string_to_list(s):
    #if s[0]== '[' and s[-1] == ']'
    return s.replace("[",'').replace(']','').replace("'",'').replace(' ','').split(",")

def pokekey(s): return s.lower().replace('-','').replace('%','').replace('*','').replace(' ','').replace('.','').replace('\"','').replace(':','')

@memoize
def defensive_resistance(defender, defender2):
    s=[[1,2,1,1,1,1,1,2**-1.5,1,1,1,1,1,1,1,1,1,1],
    [1,1,2,1,1,.5,.5,1,1,1,1,1,1,2,1,1,.5,2],
    [1,.5,1,1,2**-1.5,2,.5,1,1,1,1,.5,2,1,2,1,1,1],
    [1,.5,1,.5,2,1,.5,1,1,1,1,.5,1,2,1,1,1,.5],
    [1,1,1,.5,1,.5,1,1,1,1,2,2,2**-1.5,1,2,1,1,1],
    [.5,2,.5,.5,2,1,1,1,2,.5,2,2,1,1,1,1,1,1],
    [1,.5,2,1,.5,2,1,1,1,2,1,.5,1,1,1,1,1,1],
    [2**-1.5,2**-1.5,1,.5,1,1,.5,2,1,1,1,1,1,1,1,1,2,1],
    [.5,2,.5,.25,2,.5,.5,1,.5,2,1,.5,1,.5,.5,.5,1,.5],
    [1,1,1,1,2,2,.5,1,.5,.5,2,.5,1,1,.5,1,1,.5],
    [1,1,1,1,1,1,1,1,.5,.5,.5,2,2,1,.5,1,1,1],
    [1,1,2,2,.5,1,2,1,1,2,.5,.5,.5,1,2,1,1,1],
    [1,1,.5,1,2,1,1,1,.5,1,1,1,.5,1,1,1,1,1],
    [1,.5,1,1,1,1,2,2,1,1,1,1,1,.5,1,1,2,1],
    [1,2,1,1,1,2,1,1,2,2,1,1,1,1,.5,1,1,1],
    [1,1,1,1,1,1,1,1,1,.5,.5,.5,.5,1,2,2,1,2],
    [1,2,1,1,1,1,2,.5,1,1,1,1,1,2**-1.5,1,1,.5,2],
    [1,.5,1,2,1,1,.5,1,2,1,1,1,1,1,1,2**-1.5,.5,1]]
    e=["Normal","Fighting","Flying","Poison","Ground","Rock","Bug","Ghost",\
        "Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark","Fairy"]
    x="\t"
    t="No     Fi   Fl   Po   Gr   Ro   Bu   Gh   St   Fi   Wa   Gs   El   Ps   Ic   Dr   Da   Fa"
    for i in range(len(e)): #get attacker index
        if(e[i]==defender):
            d1_i = i
        if(e[i]==defender2):
            d2_i = i
    if(d1_i!=None and d2_i!=None):
        c = s[d1_i] #defender
    a=e[s.index(c)]
    n=a+"-"+e[d2_i]+" "
    if(e[d2_i]==a):
        n=a+"-"+a+" "
    if(c!=s[d2_i]):
        z=[float(a*b) for a,b in zip(c,s[d2_i])]
    else:
        z=c
    for b in range(18):
        n+=str(float(z[b]))+" "
    return(n.split(' ')[1:-1])

@memoize
def attack_effectiveness(att_type, def_type1, def_typ2):
    e=["Normal","Fighting","Flying","Poison","Ground","Rock","Bug","Ghost",\
        "Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark","Fairy"]
    for i in range(len(e)): #get attacker index
        if(e[i]==att_type):
            attack_index = i
    return(float(defensive_resistance(def_type1, def_typ2)[attack_index]))
