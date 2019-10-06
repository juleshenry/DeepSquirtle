import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import collections 
from functools import partial

import DataAbstract as da

#Import Data
pokedex = {}
with open('pokedex_dict.txt', 'r+') as f: exec('pokedex = ' + f.read())
df = pd.read_csv('data.csv')

#Clean Data
df = df.drop(['battle_url'],axis=1)
df = df.dropna()
df = df[df.elo != 2019]
df = df[df.elo >= 1400]
df = df[df.num_turns > 15]

#Aggregate Team Base Stats
# Defaults to All if no second argument given
# Else, takes argument team as a string and the stat in question as a string
def agg_team_basestat(stat,team):
    stats = [pokedex[da.pokekey(p)]['baseStats'] for p in da.string_to_list(team)]
    agg_stats = {}
    for i in stats:
        for j in i.keys():
            if(j not in agg_stats.keys()):
                agg_stats.update({j:i.get(j)})
            else:
                agg_stats.update({j:agg_stats.get(j) + i.get(j)})
    stat_count = 0
    for i in agg_stats.values():
        stat_count += i
    agg_stats.update({'all':stat_count})
    return agg_stats[stat]

def compare_column(func,col1,col2,new_col1,new_col2,thresh=0):
    t1_stat = df.apply(lambda x: func(x[col1]), axis=1)
    t2_stat = df.apply(lambda x: func(x[col2]), axis=1)
    df[new_col1],  df[new_col2] = t1_stat, t2_stat
    success, total = 0.0, 0.0
    for _, row in df.iterrows():
        team1 = row['agg_base_stats_1']
        team2 = row['agg_base_stats_2']
        # print(team1,'vs. ', team2,'=',row['result'])
        if(abs(team1-team2) > thresh):
            total += 1.0
            if((team1 < team2 and row['result'] == 'T2') or (team1 > team2 and row['result'] == 'T1')):
                # print('correct')
                success += 1.0
    print("Aggregate: Successes, Total, Ratio",success,total,success/total)

for t in range(0,70,5):
    print('Treshold:',t)
    compare_column(partial(agg_team_basestat,'spa'),'team_1','team_2','agg_base_stats_1','agg_base_stats_2',t)

#Type effectives
def agg_type_strength(team1,team2):
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

    return type_metric

def max_type_strength(team1,team2):
    t1 = [mon for mon in da.string_to_list(team1)]
    t2 = [mon for mon in da.string_to_list(team2)]
    t1_types = [pokedex.get(da.pokekey(mon)).get('types') for mon in t1]
    t2_types = [pokedex.get(da.pokekey(mon)).get('types') for mon in t2]
    type_metric = 0
    
    for mon1 in t1_types:
        if(len(mon1)==1): 
            for mon2 in t2_types:
                # Defending pokemon case
                if(len(mon2)==1): 
                    type_metric += np.log2(da.attack_effectiveness(mon1[0],mon2[0],mon2[0]))
                else:
                    type_metric += np.log2(da.attack_effectiveness(mon1[0],mon2[0],mon2[1]))
        else:
            for mon2 in t2_types:
                if(len(mon2)==1): 
                    type_metric += max(np.log2(da.attack_effectiveness(mon1[0],mon2[0],mon2[0])),\
                    np.log2(da.attack_effectiveness(mon1[1],mon2[0],mon2[0])))
                else:
                    type_metric += max(np.log2(da.attack_effectiveness(mon1[0],mon2[0],mon2[1])),\
                    np.log2(da.attack_effectiveness(mon1[1],mon2[0],mon2[1])))
                         
    for mon2 in t2_types:
        if(len(mon2)==1): 
            for mon1 in t1_types:
                # Defending pokemon case
                if(len(mon1)==1): 
                    type_metric -= np.log2(da.attack_effectiveness(mon2[0],mon1[0],mon1[0]))
                else:
                    type_metric -= np.log2(da.attack_effectiveness(mon2[0],mon1[0],mon1[1]))
        else:
            for mon1 in t1_types:
                if(len(mon1)==1): 
                    type_metric -= max(np.log2(da.attack_effectiveness(mon2[0],mon1[0],mon1[0])),\
                    np.log2(da.attack_effectiveness(mon2[1],mon1[0],mon1[0])))
                else:
                    type_metric -= max(np.log2(da.attack_effectiveness(mon2[0],mon1[0],mon1[1])),\
                    np.log2(da.attack_effectiveness(mon2[1],mon1[0],mon1[1])))    

    return type_metric

# df['agg_type_strength'] = df.apply(lambda x: agg_type_strength(x.team_1, x.team_2), axis=1)
# df['max_type_strength'] = df.apply(lambda x: max_type_strength(x.team_1, x.team_2), axis=1)

# success, total = 0.0,0.0
# thresh = 20
# for index, row in df.iterrows():
#     agg = row['agg_type_strength']
#     if(abs(agg) > thresh):
#         total += 1.0
#         if((agg < 0 and row['result'] == 'T2') or (agg > 0 and row['result'] == 'T1')):
#             success += 1.0

# # print("Aggregate: Successes, Total, Ratio",success,total,success/total)

# success, total = 0.0,0.0
# for index, row in df.iterrows():
#     maks = row['max_type_strength']
#     if(abs(maks) > thresh):
#         total += 1.0
#         if((maks < 0 and row['result'] == 'T2') or (maks > 0 and row['result'] == 'T1')):
#             success += 1.0

# # print("Maximum: Successes, Total, Ratio",success,total,success/total)
# for index, row in df.iterrows():
#     maks = row['max_type_strength']
#     agg = row['agg_type_strength']
#     if(abs(maks) > thresh and abs(agg) > thresh):
#         total += 1.0
#         if((maks < 0 and row['result'] == 'T2') or (maks > 0 and row['result'] == 'T1')\
#             and (agg < 0 and row['result'] == 'T2') or (agg > 0 and row['result'] == 'T1')):
#             success += 1.0

# print("Combined: Successes, Total, Ratio",success,total,success/total)
# print("Total Datapoints",df.shape[0]," Threshold",thresh)


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