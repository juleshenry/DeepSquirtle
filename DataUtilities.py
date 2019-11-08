import numpy as np
import pandas as pd

# 2**-1.5 was chosen over 0 because it is not as powerful as double resistance (2**-2) but also more advatangeous than single resistance (2**1)
def_coeffs = {
    "Normal"    : [1,2,1,1,1,1,1,2**-1.5,1,1,1,1,1,1,1,1,1,1],
    "Fighting"  : [1,1,2,1,1,.5,.5,1,1,1,1,1,1,2,1,1,.5,2],
    "Flying"    : [1,.5,1,1,2**-1.5,2,.5,1,1,1,1,.5,2,1,2,1,1,1],
    "Poison"    : [1,.5,1,.5,2,1,.5,1,1,1,1,.5,1,2,1,1,1,.5],
    "Ground"    : [1,1,1,.5,1,.5,1,1,1,1,2,2,2**-1.5,1,2,1,1,1],
    "Rock"      : [.5,2,.5,.5,2,1,1,1,2,.5,2,2,1,1,1,1,1,1],
    "Bug"       : [1,.5,2,1,.5,2,1,1,1,2,1,.5,1,1,1,1,1,1],
    "Ghost"     : [2**-1.5,2**-1.5,1,.5,1,1,.5,2,1,1,1,1,1,1,1,1,2,1],
    "Steel"     : [.5,2,.5,2**-1.5,2,.5,.5,1,.5,2,1,.5,1,.5,.5,.5,1,.5],
    "Fire"      : [1,1,1,1,2,2,.5,1,.5,.5,2,.5,1,1,.5,1,1,.5],
    "Water"     : [1,1,1,1,1,1,1,1,.5,.5,.5,2,2,1,.5,1,1,1],
    "Grass"     : [1,1,2,2,.5,1,2,1,1,2,.5,.5,.5,1,2,1,1,1],
    "Electric"  : [1,1,.5,1,2,1,1,1,.5,1,1,1,.5,1,1,1,1,1],
    "Psychic"   : [1,.5,1,1,1,1,2,2,1,1,1,1,1,.5,1,1,2,1],
    "Ice"       : [1,2,1,1,1,2,1,1,2,2,1,1,1,1,.5,1,1,1],
    "Dragon"    : [1,1,1,1,1,1,1,1,1,.5,.5,.5,.5,1,2,2,1,2],
    "Dark"      : [1,2,1,1,1,1,2,.5,1,1,1,1,1,2**-1.5,1,1,.5,2],
    "Fairy"     : [1,.5,1,2,1,1,.5,1,2,1,1,1,1,1,1,2**-1.5,.5,1]
}

def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func

def get_roster_as_list(s):
    bad_chars = ['[', ']', "'", ' ']
    return s.translate({ord(c): '' for c in bad_chars}).split(',')

def pokekey(s):
    bad_chars = ['-', '%', '*', '.', ' ', ':', '\"']
    return s.lower().translate({ord(c): '' for c in bad_chars})

def poke_defend(types):
    return types if len(types) == 2 else [types[0], types[0]]

def get_defense_effectiveness_list(def_type_1, def_type_2):
    if def_type_1 == def_type_2:
        return def_coeffs[def_type_1]

    return [float(a*b) for a,b in zip(def_coeffs[def_type_1], def_coeffs[def_type_2])]


def get_attack_effectiveness(att_mon_type, def_mon_types):
    def_mon_types = poke_defend(def_mon_types)
    type_indices = list(def_coeffs.keys())

    att_index = type_indices.index(att_mon_type)

    return get_defense_effectiveness_list(*def_mon_types)[att_index]

#TODO: Get distributions possibly pickle, possible memoize, implement correctly
def get_usage_distributions():
    return
    # agg_roster = []
    # for i in range(2000):
    #     agg_roster += [mon for mon in da.string_to_list(df.team_1.iloc[i])]
    #     agg_roster += [mon for mon in da.string_to_list(df.team_2.iloc[i])]
    # roster_freq = {}
    # for mon in agg_roster:
    #     if(mon not in roster_freq.keys()):
    #         roster_freq.update({mon:1})
    #     else:
    #         roster_freq.update({mon:roster_freq.get(mon)+1})
    # dict_roster_freq = collections.OrderedDict(sorted(roster_freq.items(),key = lambda kv: kv[1]))
    # samplesize = 0
    # freq_key_list = list(dict_roster_freq.keys())
    # freq_val_list = list(dict_roster_freq.values())
    # for freq in freq_val_list: samplesize += freq
    # for i in range(40):
    #     print(f"{i+1}. {freq_key_list[-i-1]} : {freq_val_list[-i-1]*100/samplesize}%")

    # plt.bar(dict_roster_freq.keys(),dict_roster_freq.values(),color='g')
    # plt.xticks(rotation=90)
    # plt.show()
    # x = [pokedex[da.pokekey(p)]['types'] for p in da.string_to_list(df.team_1.iloc[0])]