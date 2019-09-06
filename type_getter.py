import json
import pandas as pd

showdata = pd.read_csv('data.csv')

test = '''{chansey: {
		num: 113,
		species: "Chansey",
		types: ["Normal"],
		gender: "F",
		baseStats: {hp: 250, atk: 5, def: 5, spa: 35, spd: 105, spe: 50},
		abilities: {0: "Natural Cure", 1: "Serene Grace", H: "Healer"},
		heightm: 1.1,
		weightkg: 34.6,
		color: "Pink",
		prevo: "happiny",
		evoType: "levelHold",
		evoItem: "Oval Stone",
		evoCondition: "during the day",
		evos: ["blissey"],
		eggGroups: ["Fairy"],
		canHatch: true,
	}'''
def insert (source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def javascript_dict_to_python(s): #TODO address boolean format, address errant quotes
    within_word = False
    s = s.replace('\"','')
    quote_indices = []
    for i in range(0,len(s)-1): 
        if s[i+1].isalpha() and (not within_word):
            quote_indices.append(i+1)
            within_word = not within_word
        elif (not s[i+1].isalpha()) and within_word:
            quote_indices.append(i+1)
            within_word = not within_word
    for i in reversed(quote_indices): s = insert(s, '\'', i)
    for i in range(len(quote_indices[:-1])):
        print(s[quote_indices[i]:quote_indices[i+1]])
    return s
    
print(javascript_dict_to_python(test)) 

# f = open('pokedex_dict.txt', 'w+')
# f.write(js_dex)
# f.close
# with open('pokedex_dict.txt', 'r') as f:
#     data_dict = exec(f.read)