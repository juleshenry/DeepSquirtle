import numpy as np
import pandas as pd
from DataUtilities import *
from collections import Counter

class DataTransformer:

    def __init__(self):
        self.pokedex = {}

        with open('pokedex_dict.txt', 'r+', encoding='utf-8') as f: exec('self.pokedex = ' + f.read())
        self.usage_dict = {} #when this is a variable of the class, it does not have to be recalculated. Otherwise, add to DataUtilities and pickle!
    
    def transform(self, data):

        # Initialize Usage_Dictionary
        self.usage_dict = self.get_usage_dict(data)

        data['highest_speed_flag'] = data.apply(lambda row: self.get_highest_speed_flag(row['team_1'],row['team_2']),axis=1)

        data['mean_roster_usage_rates_1'] = data.apply(lambda row: self.get_mean_roster_usage_rates(row['team_1']),axis=1)
        data['mean_roster_usage_rates_2'] = data.apply(lambda row: self.get_mean_roster_usage_rates(row['team_2']),axis=1)

        data['most_effective_attack_effectiveness'] = data.apply(lambda row: self.get_most_effective_attack_effectiveness(row['team_1'],row['team_2']),axis=1)
        
        data['roster_mean_all_stats_1'] = data.apply(lambda row: self.get_roster_mean_all_stats(row['team_1']),axis=1)
        data['roster_mean_all_stats_2'] = data.apply(lambda row: self.get_roster_mean_all_stats(row['team_2']),axis=1)

        stats_list = ['hp','atk','def','spa','spd','hp']
        for stat in stats_list:
            data['roster_mean_basestat_1_'+stat] = data.apply(lambda row: self.get_roster_mean_basestat(stat,row['team_1']),axis=1)
            data['roster_mean_basestat_2_'+stat] = data.apply(lambda row: self.get_roster_mean_basestat(stat,row['team_2']),axis=1)

        # get_roster_mean_overall_attack
        # 'get_roster_mean_overall_attack',
        # 'get_roster_mean_overall_defense',
        # 'get_roster_median_basestat',
        # 'get_roster_sdv_all_stats'
        # 'get_roster_sdv_basestat',
        # 'get_roster_sdv_overall_attack',
        # 'get_roster_sdv_overall_defense',
        # 'get_sdv_roster_usage_rates',
        # 'get_total_attack_effectiveness',
        print(data.head())
        return data

    # Returns a dictionary with keys as pokemon and usage as percentage of total appearance as values
    def get_usage_dict(self, data):
        usage_dict = {}

        for i in range(data.shape[0]):
            teams = ['team_1','team_2']
            for team in teams:
                for poke in get_roster_as_list(data[team].iloc[i]):
                    poke = deforme_pokemon_name(poke)
                    if poke in usage_dict.keys():
                        usage_dict.update({poke : usage_dict.get(poke) + 1})
                    else:
                        usage_dict.update({poke : 1})

        total = 0
        for cnt in usage_dict.values():
            total = total + cnt

        for j in usage_dict.keys():
            usage_dict.update({j : float(usage_dict.get(j))/total})
            # print(j,float(usage_dict.get(j)*100),'%')
        return usage_dict

    def get_roster_mean_basestat(self, stat, roster):
        return sum([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(roster)])/6.0

    def get_roster_mean_all_stats(self, roster):
        m_hp = self.get_roster_mean_basestat('hp', roster)
        m_atk = self.get_roster_mean_basestat('atk', roster)
        m_def = self.get_roster_mean_basestat('def', roster)
        m_spa = self.get_roster_mean_basestat('spa', roster)
        m_spd = self.get_roster_mean_basestat('spd', roster)
        m_spe = self.get_roster_mean_basestat('spe', roster)
        
        return (m_hp + m_atk + m_def + m_spa + m_spd + m_spe)/6.0

    def get_roster_mean_overall_defense(self, stat, roster):
        m_hp = self.get_roster_mean_basestat('hp', roster)
        m_def = self.get_roster_mean_basestat('def', roster)
        m_spd = self.get_roster_mean_basestat('spd', roster)
        return (m_hp + m_def + m_spd)/3.0

    def get_roster_mean_overall_attack(self, stat, roster):
        m_atk = self.get_roster_mean_basestat('atk', roster)
        m_spa = self.get_roster_mean_basestat('spa', roster)
        return (m_atk + m_spa)/2.0

    def get_roster_sdv_basestat(self, stat, roster):
        return np.std([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(roster)])
    
    def get_roster_median_basestat(self, stat, roster):
        return np.median([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(roster)])

    def get_roster_sdv_all_stats(self, stat, roster):
        sdv_hp = self.get_roster_sdv_basestat('hp', roster)
        sdv_atk = self.get_roster_sdv_basestat('atk', roster)
        sdv_def = self.get_roster_sdv_basestat('def', roster)
        sdv_spa = self.get_roster_sdv_basestat('spa', roster)
        sdv_spd = self.get_roster_sdv_basestat('spd', roster)
        sdv_spe = self.get_roster_sdv_basestat('spe', roster)

        return (sdv_hp + sdv_atk + sdv_def + sdv_spa + sdv_spd + sdv_spe)/6.0

    def get_roster_sdv_overall_defense(self, stat, roster):
        sdv_hp = self.get_roster_sdv_basestat('hp', roster)
        sdv_def = self.get_roster_sdv_basestat('def', roster)
        sdv_spd = self.get_roster_sdv_basestat('spd', roster)
        return (sdv_hp + sdv_def + sdv_spd)/3.0

    def get_roster_sdv_overall_attack(self, stat, roster):
        sdv_atk = self.get_roster_sdv_basestat('atk', roster)
        sdv_spa = self.get_roster_sdv_basestat('spa', roster)
        return (sdv_atk + sdv_spa)/2.0

    def get_total_attack_effectiveness(self, roster1, roster2):
        t1 = [mon for mon in get_roster_as_list(roster1)]
        t2 = [mon for mon in get_roster_as_list(roster2)]
        t1_as_types = [self.pokedex.get(pokekey(mon)).get('types') for mon in t1]
        t2_as_types = [self.pokedex.get(pokekey(mon)).get('types') for mon in t2]

        type_metric = 0

        for att_mon_types in t1_as_types:
            for def_mon_types in t2_as_types:
                type_metric += self.evaluate_matchup_total(att_mon_types, def_mon_types)

        for att_mon_types in t2_as_types:
            for def_mon_types in t1_as_types:
                type_metric -= self.evaluate_matchup_total(att_mon_types, def_mon_types)

        return type_metric

    # Is positive if in favor of roster_1
    def get_most_effective_attack_effectiveness(self, roster1, roster2):
        t1 = get_roster_as_list(roster1)
        t2 = get_roster_as_list(roster2)
        t1_as_types = [self.pokedex.get(pokekey(mon)).get('types') for mon in t1]
        t2_as_types = [self.pokedex.get(pokekey(mon)).get('types') for mon in t2]

        type_metric = 0

        for att_mon_types in t1_as_types:
            for def_mon_types in t2_as_types:
                type_metric += self.evaluate_matchup_most_effective(att_mon_types, def_mon_types)

        for att_mon_types in t2_as_types:
            for def_mon_types in t1_as_types:
                type_metric -= self.evaluate_matchup_most_effective(att_mon_types, def_mon_types)

        return type_metric
    
    def get_highest_speed_flag(self, roster1, roster2):
        fastest_1 = max([self.pokedex[pokekey(p)]['baseStats']['spe'] for p in get_roster_as_list(roster1)])
        fastest_2 = max([self.pokedex[pokekey(p)]['baseStats']['spe'] for p in get_roster_as_list(roster2)])
        return 'T1' if fastest_1 > fastest_2 else 'T2' if fastest_2 > fastest_1 else 'TIE'
  
    def get_sdv_roster_usage_rates(self, roster):
        return np.std([self.usage_dict[deforme_pokemon_name(mon)] for mon in get_roster_as_list(roster)])

    def get_mean_roster_usage_rates(self, roster):
        return sum([self.usage_dict[deforme_pokemon_name(mon)] for mon in get_roster_as_list(roster)]) / 6.0

    def evaluate_matchup_total(self, att_mon_types, def_mon_types):
        if len(att_mon_types) == 1:
            return get_attack_effectiveness(att_mon_types[0], def_mon_types)

        else:
            return sum(get_attack_effectiveness(att_mon_types[0], def_mon_types),
                       get_attack_effectiveness(att_mon_types[1], def_mon_types))

    def evaluate_matchup_most_effective(self, att_mon_types, def_mon_types):
        if len(att_mon_types) == 1:
            return get_attack_effectiveness(att_mon_types[0], def_mon_types)
        else:
            return max(get_attack_effectiveness(att_mon_types[0], def_mon_types),
                       get_attack_effectiveness(att_mon_types[1], def_mon_types))
