import numpy as np
import pandas as pd
from DataUtilites import *

class DataTransformer:
    def __init__(self):
        with open('pokedex_dict.txt', 'r+') as f: exec('self.pokedex = ' + f.read())

    def transform(self, data):
        pass

    def get_roster_mean_basestat(self, stat, roster):
        return sum([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(roster)])/6.0

    def get_roster_mean_all_stats(self, roster):
        m_hp = get_roster_mean_basestat('hp', roster)
        m_atk = get_roster_mean_basestat('atk', roster)
        m_def = get_roster_mean_basestat('def', roster)
        m_spa = get_roster_mean_basestat('spa', roster)
        m_spd = get_roster_mean_basestat('spd', roster)
        m_spe = get_roster_mean_basestat('spe', roster)

        return (m_hp + m_atk + m_def + m_spa + m_spd + m_spe)/6.0

    def get_roster_sdv_basestat(self, stat, roster):
        return np.std([self.pokedex[pokekey(p)]['baseStats'][stat] for p in get_roster_as_list(roster)])

    def get_roster_sdv_all_stats(self, stat, roster):
        ''' Pretty sure that this statistic is flawed... it is currently
            a mean of the standard deviations of all statistics. I imagine
            that when not normalized, certain statistics can dominate this metric,
            thus diluting its value. Follow up on this '''
        sdv_hp = get_roster_sdv_basestat('hp', roster)
        sdv_atk = get_roster_sdv_basestat('atk', roster)
        sdv_def = get_roster_sdv_basestat('def', roster)
        sdv_spa = get_roster_sdv_basestat('spa', roster)
        sdv_spd = get_roster_sdv_basestat('spd', roster)
        sdv_spe = get_roster_sdv_basestat('spe', roster)

        return (sdv_hp + sdv_atk + sdv_def + sdv_spa + sdv_spd + sdv_spe)/6.0

    def get_total_attack_effectiveness(self, roster1, roster2):
        t1 = [mon for mon in get_roster_as_list(team1)]
        t2 = [mon for mon in get_roster_as_list(team2)]
        t1_types = [pokedex.get(pokekey(mon)).get('types') for mon in t1]
        t2_types = [pokedex.get(pokekey(mon)).get('types') for mon in t2]

        type_metric = 0

        for att_mon_types in t1_as_types:
            for def_mon_types in t2_as_types:
                type_metric += self.evaluate_matchup_most_effective(att_mon_types, def_mon_types)

        for att_mon_types in t2_as_types:
            for def_mon_types in t1_as_types:
                type_metric -= self.evaluate_matchup_most_effective(att_mon_types, def_mon_types)

        return type_metric

    def get_most_effective_attack_effectiveness(self, roster1, roster2):
        t1 = [mon for mon in get_roster_as_list(roster1)]
        t2 = [mon for mon in get_roster_as_list(roster2)]
        t1_as_types = [pokedex.get(pokekey(mon)).get('types') for mon in t1]
        t2_as_types = [pokedex.get(pokekey(mon)).get('types') for mon in t2]

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
