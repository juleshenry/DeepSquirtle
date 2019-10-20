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
df = df[df.num_turns > 5] #TODO: could be deviation from mean turns

#Aggregate Team Base Stats
# Defaults to All if no second argument given
# Else, takes argument team as a string and the stat in question as a string
# 'hp',  'atk', 'def', 'spa', 'spd', 'spe'}
def mean_team_basestat(stat,team):
    stats = [pokedex[da.pokekey(p)]['baseStats'] for p in da.string_to_list(team)]
    mean_stats = {}
    # construct stat aggregate dictionary
    for i in stats:
        for j in i.keys():
            if(j not in mean_stats.keys()):
                mean_stats.update({j:i.get(j)})
            else:
                mean_stats.update({j:mean_stats.get(j) + i.get(j)})
    # average each stat
    for k in mean_stats.keys():
        mean_stats.update({k : mean_stats[k]/6.0})
    # summing all stats            
    stat_count = 0
    for i in mean_stats.values():
        stat_count += i
    mean_stats.update({'all':float(stat_count)/6.0})
    return mean_stats[stat]

def sdv_team_basestat(stat,team):
    stats = [pokedex[da.pokekey(p)]['baseStats'] for p in da.string_to_list(team)]
    sdv_stats = {}
    # construct stat aggregate dictionary
    for i in stats:
        for j in i.keys():
            if(j not in sdv_stats.keys()):
                sdv_stats.update({j : [i.get(j),0,0,0,0,0] })
            else:
                s = sdv_stats.get(j)
                s[s.index(0)] = i.get(j)
                sdv_stats.update({j : s})

    # sdv each stat
    for k in sdv_stats.keys(): 
        sdv_stats.update({k : np.std(sdv_stats[k])})

    #sdv of all stats
    stat_count = 0
    for i in sdv_stats.values():
        stat_count += i
    sdv_stats.update({'all':float(stat_count)/6.0})
    return sdv_stats[stat]
    
def compare_column(func,col1,col2,new_col1,new_col2,thresh=0):
    t1_stat = df.apply(lambda x: func(x[col1]), axis=1)
    t2_stat = df.apply(lambda x: func(x[col2]), axis=1)
    df[new_col1],  df[new_col2] = t1_stat, t2_stat #TODO: change from global variable
    success, total = 0.0, 0.0
    for _, row in df.iterrows():
        team1_stat = row[new_col1]
        team2_stat = row[new_col2]
        # print(team1_stat,'vs. ', team2_stat,'=',row['result'])
        if(abs(team1_stat-team2_stat) > thresh):
            total += 1.0
            if((team1_stat < team2_stat and row['result'] == 'T2') or (team1_stat > team2_stat and row['result'] == 'T1')):
                # print('correct')
                success += 1.0
    print("Aggregate: Successes, Total, Ratio\n",success,total,success/total)
    return success/total

l_hp, l_atk, l_def, l_spa, l_spd, l_spe, l_all = [],[],[],[],[],[],[]
plot_thresh = []

for t in range(0,31,5):
    print('Threshold:',t)
    plot_thresh += [t]
    l_hp += [compare_column(partial(sdv_team_basestat,'hp'),'team_1','team_2','mean_base_stats_1','mean_base_stats_2',t)]
    l_atk += [compare_column(partial(sdv_team_basestat,'atk'),'team_1','team_2','mean_base_stats_1','mean_base_stats_2',t)]
    l_def += [compare_column(partial(sdv_team_basestat,'def'),'team_1','team_2','mean_base_stats_1','mean_base_stats_2',t)]
    l_spa += [compare_column(partial(sdv_team_basestat,'spa'),'team_1','team_2','mean_base_stats_1','mean_base_stats_2',t)]
    l_spd += [compare_column(partial(sdv_team_basestat,'spd'),'team_1','team_2','mean_base_stats_1','mean_base_stats_2',t)]
    l_spe += [compare_column(partial(sdv_team_basestat,'spe'),'team_1','team_2','mean_base_stats_1','mean_base_stats_2',t)]
    l_all += [compare_column(partial(sdv_team_basestat,'all'),'team_1','team_2','mean_base_stats_1','mean_base_stats_2',t)]

plt.plot(plot_thresh, l_hp, label='hp')
plt.plot(plot_thresh, l_atk, label='atk')
plt.plot(plot_thresh, l_def, label='def')
plt.plot(plot_thresh, l_spa, label='spa')
plt.plot(plot_thresh, l_spd, label='spd')
plt.plot(plot_thresh, l_spe, label='spe')
plt.plot(plot_thresh, l_all, label='all')
plt.legend(loc='best')
plt.show()

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

# plot_thresh, plot_agg, plot_max, plot_comb = [], [], [], []
# for thresh in range(0,31,2):

#     print('Threshold:',thresh)
#     plot_thresh.append(thresh)

#     success, total = 0.0,0.0
#     for index, row in df.iterrows():
#         agg = row['agg_type_strength']
#         if(abs(agg) > thresh):
#             total += 1.0
#             if((agg < 0 and row['result'] == 'T2') or (agg > 0 and row['result'] == 'T1')):
#                 success += 1.0

#     print("Aggregate: Successes, Total, Ratio\n",success,total,success/total)
#     plot_agg.append(success/total)

#     success, total = 0.0,0.0
#     for index, row in df.iterrows():
#         maks = row['max_type_strength']
#         if(abs(maks) > thresh):
#             total += 1.0
#             if((maks < 0 and row['result'] == 'T2') or (maks > 0 and row['result'] == 'T1')):
#                 success += 1.0

#     print("Maximum: Successes, Total, Ratio\n",success,total,success/total)
#     plot_max.append(success/total)

#     success, total = 0.0,0.0
#     for index, row in df.iterrows():
#         maks = row['max_type_strength']
#         agg = row['agg_type_strength']
#         if(abs(maks) > thresh and abs(agg) > thresh):
#             total += 1.0
#             if((maks < 0 and row['result'] == 'T2') or (maks > 0 and row['result'] == 'T1')\
#                 and (agg < 0 and row['result'] == 'T2') or (agg > 0 and row['result'] == 'T1')):
#                 success += 1.0

#     print("Combined: Successes, Total, Ratio\n",success,total,success/total)
#     plot_comb.append(success/total)

#     print("Total Datapoints",df.shape[0]," Threshold",thresh)



# plt.plot(plot_thresh, plot_agg, label='agg')
# plt.plot(plot_thresh, plot_max, label='max')
# plt.plot(plot_thresh, plot_comb, label='comb')
# plt.legend(loc='best')
# plt.show()

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