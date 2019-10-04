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
stats = [pokedex[da.pokekey(p)]['baseStats'] for p in da.string_to_list(df.team_1.iloc[0])]
agg_stats = {}
for i in stats:
    for j in i.keys():
        if(j not in agg_stats.keys()):
            agg_stats.update({j:i.get(j)})
        else:
            agg_stats.update({j:agg_stats.get(j) + i.get(j)})

#Type effectives
def agg_type_strength(team1,team2):
    print(team1,team2)
    t1 = [mon for mon in da.string_to_list(team1)]
    t2 = [mon for mon in da.string_to_list(team2)]
    t1_types = [pokedex.get(da.pokekey(mon)).get('types') for mon in t1]
    t2_types = [pokedex.get(da.pokekey(mon)).get('types') for mon in t2]

    type_metric = 0
    for mon1 in t1_types:
        for att_type in mon1:
            for mon2 in t2_types:
                if(len(mon2)==1): 
                    type_metric += np.log2(da.attack_effectiveness(att_type,mon2[0],mon2[0]))
                else:
                    type_metric += np.log2(da.attack_effectiveness(att_type,mon2[0],mon2[1]))
                            
    for mon2 in t2_types:
        for att_type in mon2:
            for mon1 in t1_types:
                if(len(mon1)==1): 
                    type_metric -= np.log2(da.attack_effectiveness(att_type,mon1[0],mon1[0]))
                else:
                    type_metric -= np.log2(da.attack_effectiveness(att_type,mon1[0],mon1[1]))

    return(type_metric)

df['agg_type_strength'] = df.apply(lambda x: agg_type_strength(x.team_1, x.team_2), axis=1)

print(df['agg_type_strength'].to_frame().head())

#Calculate Distribution of Pokemon
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