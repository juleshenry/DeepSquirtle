import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import collections 

import DataAbstract as da

#Import Data
pokedex = {}
with open('pokedex_dict.txt', 'r+') as f: exec('pokedex = ' + f.read())
df = pd.read_csv('data.csv')

#Clean Data
df = df.drop(['battle_url'],axis=1)
df = df.dropna()
df = df[df.elo != 2019]
df = df[df.num_turns > 15]

#Aggregate Team Base Stats
stats = [pokedex[da.pokekey(p)]['baseStats'] for p in da.destring(df.team_1.iloc[0])]
agg_stats = {}
for i in stats:
    for j in i.keys():
        if(j not in agg_stats.keys()):
            agg_stats.update({j:i.get(j)})
        else:
            agg_stats.update({j:agg_stats.get(j) + i.get(j)})

t1 = [mon for mon in da.destring(df.team_1.iloc[100])]
t2 = [mon for mon in da.destring(df.team_2.iloc[100])]
t1_types = [pokedex.get(da.pokekey(mon)).get('types') for mon in t1]
t2_types = [pokedex.get(da.pokekey(mon)).get('types') for mon in t2]

print(str(t1)+' VS. '+str(t2))
t1_metric = 0

for mon1 in t1_types:
    for att_type in mon1:
        for mon2 in t2_types:
            if(len(mon2)==1): 
                t1_metric += np.log2(da.attack_effectiveness(att_type,mon2[0],mon2[0]))
            else:
                t1_metric += np.log2(da.attack_effectiveness(att_type,mon2[0],mon2[1]))

for mon2 in t2_types:
    for att_type in mon2:
        for mon1 in t1_types:
            if(len(mon1)==1): 
                t1_metric -= np.log2(da.attack_effectiveness(att_type,mon1[0],mon1[0]))
            else:
                t1_metric -= np.log2(da.attack_effectiveness(att_type,mon1[0],mon1[1]))

print(t1_metric)
#for the types, calculates 36+ combos
#produce a single number




#Calculate Distribution of Pokemon
# agg_roster = []
# for i in range(2000):
#     agg_roster += [mon for mon in da.destring(df.team_1.iloc[i])]
#     agg_roster += [mon for mon in da.destring(df.team_2.iloc[i])]
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
#Type Effectiveness Metric
# print(da.attack_effectiveness('Fire','Grass','Ice'))




# plt.bar(dict_roster_freq.keys(),dict_roster_freq.values(),color='g')
# plt.xticks(rotation=90)
# plt.show()
# x = [pokedex[da.pokekey(p)]['types'] for p in da.destring(df.team_1.iloc[0])]