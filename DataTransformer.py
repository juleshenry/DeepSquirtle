import numpy as np
import pandas as pd
from DataUtilities import *
from collections import Counter

class DataTransformer:

    def __init__(self):
        self.pokedex = {}
        with open('pokedex_dict.txt', 'r+') as f: exec('self.pokedex = ' + f.read())
        self.usage_dict = {}
    
    def transform(self, data):
        # Initialize Usage_Dictionary
        self.usage_dict = self.get_usage_dict(data)

        transformed_data = data 

        return transformed_data

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
            # print(j,float(usage_dict.get(j)*100))
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

    def get_roster_sdv_basestat(self, stat, roster):
        return np.std([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(roster)])

    def get_roster_sdv_all_stats(self, stat, roster):
        ''' Pretty sure that this statistic is flawed... it is currently
            a mean of the standard deviations of all statistics. I imagine
            that when not normalized, certain statistics can dominate this metric,
            thus diluting its value. Follow up on this '''
        sdv_hp = self.get_roster_sdv_basestat('hp', roster)
        sdv_atk = self.get_roster_sdv_basestat('atk', roster)
        sdv_def = self.get_roster_sdv_basestat('def', roster)
        sdv_spa = self.get_roster_sdv_basestat('spa', roster)
        sdv_spd = self.get_roster_sdv_basestat('spd', roster)
        sdv_spe = self.get_roster_sdv_basestat('spe', roster)

        return (sdv_hp + sdv_atk + sdv_def + sdv_spa + sdv_spd + sdv_spe)/6.0

    def get_total_attack_effectiveness(self, roster1, roster2):
        t1 = [mon for mon in get_roster_as_list(roster1)]
        t2 = [mon for mon in get_roster_as_list(roster2)]
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

    def get_highest_speed_flag(self, roster1, roster2):
        # t1 = [mon for mon in get_roster_as_list(roster1)]
        # t2 = [mon for mon in get_roster_as_list(roster2)]
        # t1_as_types = [self.pokedex.get(pokekey(mon)).get('baseStats').get('spe') for mon in t1]
        # t2_as_types = [self.pokedex.get(pokekey(mon)).get('baseStats').get('spe') for mon in t2]
        return 
  
    def get_sdv_roster_usage_rates(self, roster):
        return np.std([self.usage_dict[deforme_pokemon_name(mon)] for mon in get_roster_as_list(roster)])

    def get_mean_roster_usage_rates(self, roster):
        return sum([self.usage_dict[deforme_pokemon_name(mon)] for mon in get_roster_as_list(roster)]) / 6.0

