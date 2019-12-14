import numpy as np
import pandas as pd
import inspect
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

        data['total_effective_attack_effectiveness'] = data.apply(lambda row: self.get_total_attack_effectiveness(row['team_1'],row['team_2']),axis=1)
        data['highest_speed_flag'] = data.apply(lambda row: self.get_highest_speed_flag(row['team_1'],row['team_2']),axis=1)

        data['mean_roster_usage_rates_1'] = data.apply(lambda row: self.get_mean_roster_usage_rates(row['team_1']),axis=1)
        data['mean_roster_usage_rates_2'] = data.apply(lambda row: self.get_mean_roster_usage_rates(row['team_2']),axis=1)

        data['sdv_roster_usage_rates_1'] = data.apply(lambda row: self.get_sdv_roster_usage_rates(row['team_1']),axis=1)
        data['sdv_roster_usage_rates_2'] = data.apply(lambda row: self.get_sdv_roster_usage_rates(row['team_2']),axis=1)

        data['most_effective_attack_effectiveness'] = data.apply(lambda row: self.get_most_effective_attack_effectiveness(row['team_1'],row['team_2']),axis=1)
        data['total_effective_attack_effectiveness'] = data.apply(lambda row: self.get_total_attack_effectiveness(row['team_1'],row['team_2']),axis=1)
        
        data['roster_mean_all_stats_1'] = data.apply(lambda row: self.get_roster_mean_all_stats(row['team_1']),axis=1)
        data['roster_mean_all_stats_2'] = data.apply(lambda row: self.get_roster_mean_all_stats(row['team_2']),axis=1)

        data['roster_mean_overall_attack_1'] = data.apply(lambda row: self.get_roster_mean_overall_attack(row['team_1']),axis=1)
        data['roster_mean_overall_attack_2'] = data.apply(lambda row: self.get_roster_mean_overall_attack(row['team_2']),axis=1)

        data['roster_mean_overall_defense_1'] = data.apply(lambda row: self.get_roster_mean_overall_defense(row['team_1']),axis=1)
        data['roster_mean_overall_defense_2'] = data.apply(lambda row: self.get_roster_mean_overall_defense(row['team_2']),axis=1)

        data['roster_sdv_all_stats_1'] = data.apply(lambda row: self.get_roster_sdv_all_stats(row['team_1']),axis=1)
        data['roster_sdv_all_stats_1'] = data.apply(lambda row: self.get_roster_sdv_all_stats(row['team_1']),axis=1)

        data['roster_sdv_overall_attack_1'] = data.apply(lambda row: self.get_roster_sdv_overall_attack(row['team_1']),axis=1)
        data['roster_sdv_overall_attack_2'] = data.apply(lambda row: self.get_roster_sdv_overall_attack(row['team_2']),axis=1)

        data['roster_sdv_overall_defense_1'] = data.apply(lambda row: self.get_roster_sdv_overall_defense(row['team_1']),axis=1)
        data['roster_sdv_overall_defense_1'] = data.apply(lambda row: self.get_roster_sdv_overall_defense(row['team_1']),axis=1)
       
        for stat in ['hp','atk','def','spa','spd','hp']:
            data['roster_mean_basestat_1_'+stat] = data.apply(lambda row: self.get_roster_mean_basestat(stat,row['team_1']),axis=1)
            data['roster_mean_basestat_2_'+stat] = data.apply(lambda row: self.get_roster_mean_basestat(stat,row['team_2']),axis=1)
            data['roster_sdv_basestat_1_'+stat] = data.apply(lambda row: self.get_roster_sdv_basestat(stat,row['team_1']),axis=1)
            data['roster_sdv_basestat_2_'+stat] = data.apply(lambda row: self.get_roster_sdv_basestat(stat,row['team_2']),axis=1)
            data['roster_median_basestat_1_'+stat] = data.apply(lambda row: self.get_roster_median_basestat(stat,row['team_1']),axis=1)
            data['roster_median_basestat_2_'+stat] = data.apply(lambda row: self.get_roster_median_basestat(stat,row['team_2']),axis=1)

        droppable_columns = ['team_1', 'team_2', 'num_turns','disconnect']
        return data.drop(droppable_columns, axis=1)

    def transform_from_class_dict(self, data):
        # Initialize Usage_Dictionary
        self.usage_dict = self.get_usage_dict(data)
        func_args_list = [[getattr(self, func), tuple_to_list(str(inspect.signature(getattr(self, func))))] \
                         for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]

        disqualifying_args = set()
        for args in func_args_list:
            for arg in args[1]:
                if arg not in str(data.columns.tolist()):
                    disqualifying_args.add(arg)

        for func_arg in func_args_list:
            func, arg, safe = func_arg[0], func_arg[1], True
            for dq_arg in disqualifying_args: # One argument is not in the dataset columns 
                if dq_arg in arg: safe = False
            if safe: 
                if 'team_1' in arg and 'team_2' in arg and len(arg) == 2: # Column metric describes both teams
                    data[func.__name__] = data.apply(lambda row: func(row['team_1'],row['team_2']),axis=1)
                else:
                    data[func.__name__ + '_1'] = data.apply(lambda row: func(row['team_1']),axis=1)
                    data[func.__name__ + '_2'] = data.apply(lambda row: func(row['team_2']),axis=1)
            else:
                if 'stat' in arg:
                    for stat in ['hp','atk','def','spa','spd','hp']:
                        data[func.__name__+'_1_'+stat] = data.apply(lambda row: func(stat,row['team_1']),axis=1)
                        data[func.__name__+'_2_'+stat] = data.apply(lambda row: func(stat,row['team_2']),axis=1)
        
        droppable_columns = ['team_1', 'team_2', 'num_turns','disconnect']
        return data.drop(droppable_columns, axis=1)

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

    def get_roster_mean_basestat(self, stat, team_1):
        return sum([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(team_1)])/6.0

    def get_roster_mean_all_stats(self, team_1):
        m_hp = self.get_roster_mean_basestat('hp', team_1)
        m_atk = self.get_roster_mean_basestat('atk', team_1)
        m_def = self.get_roster_mean_basestat('def', team_1)
        m_spa = self.get_roster_mean_basestat('spa', team_1)
        m_spd = self.get_roster_mean_basestat('spd', team_1)
        m_spe = self.get_roster_mean_basestat('spe', team_1)
        
        return (m_hp + m_atk + m_def + m_spa + m_spd + m_spe)/6.0

    def get_roster_mean_overall_defense(self, team_1):
        m_hp = self.get_roster_mean_basestat('hp', team_1)
        m_def = self.get_roster_mean_basestat('def', team_1)
        m_spd = self.get_roster_mean_basestat('spd', team_1)
        return (m_hp + m_def + m_spd)/3.0

    def get_roster_mean_overall_attack(self, team_1):
        m_atk = self.get_roster_mean_basestat('atk', team_1)
        m_spa = self.get_roster_mean_basestat('spa', team_1)
        return (m_atk + m_spa)/2.0

    def get_roster_sdv_basestat(self, stat, team_1):
        return np.std([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(team_1)])
    
    def get_roster_median_basestat(self, stat, team_1):
        return np.median([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(team_1)])

    def get_roster_sdv_all_stats(self, team_1):
        sdv_hp = self.get_roster_sdv_basestat('hp', team_1)
        sdv_atk = self.get_roster_sdv_basestat('atk', team_1)
        sdv_def = self.get_roster_sdv_basestat('def', team_1)
        sdv_spa = self.get_roster_sdv_basestat('spa', team_1)
        sdv_spd = self.get_roster_sdv_basestat('spd', team_1)
        sdv_spe = self.get_roster_sdv_basestat('spe', team_1)

        return (sdv_hp + sdv_atk + sdv_def + sdv_spa + sdv_spd + sdv_spe)/6.0

    def get_roster_sdv_overall_defense(self, team_1):
        sdv_hp = self.get_roster_sdv_basestat('hp', team_1)
        sdv_def = self.get_roster_sdv_basestat('def', team_1)
        sdv_spd = self.get_roster_sdv_basestat('spd', team_1)
        return (sdv_hp + sdv_def + sdv_spd)/3.0

    def get_roster_sdv_overall_attack(self, team_1):
        sdv_atk = self.get_roster_sdv_basestat('atk', team_1)
        sdv_spa = self.get_roster_sdv_basestat('spa', team_1)
        return (sdv_atk + sdv_spa)/2.0

    # Returns positive if in favor of roster_1
    def get_total_attack_effectiveness(self, team_1, team_2):
        t1 = get_roster_as_list(team_1)
        t2 = get_roster_as_list(team_2)
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

    # Returns positive if in favor of roster_1
    def get_most_effective_attack_effectiveness(self, team_1, team_2):
        t1 = get_roster_as_list(team_1)
        t2 = get_roster_as_list(team_2)
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
    
    def get_highest_speed_flag(self, team_1, team_2):
        fastest_1 = max([self.pokedex[pokekey(p)]['baseStats']['spe'] for p in get_roster_as_list(team_1)])
        fastest_2 = max([self.pokedex[pokekey(p)]['baseStats']['spe'] for p in get_roster_as_list(team_2)])
        return 'T1' if fastest_1 > fastest_2 else 'T2' if fastest_2 > fastest_1 else 'TIE'
  
    def get_sdv_roster_usage_rates(self, team_1):
        return np.std([self.usage_dict[deforme_pokemon_name(mon)] for mon in get_roster_as_list(team_1)])

    def get_mean_roster_usage_rates(self, team_1):
        return sum([self.usage_dict[deforme_pokemon_name(mon)] for mon in get_roster_as_list(team_1)]) / 6.0

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
