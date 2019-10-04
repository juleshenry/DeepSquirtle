import json
import pandas as pd

pokedex_js = ''
notcare = ['num:', 'gender', 'heightm', 'color', 'prevo', 'evoType', \
    'evoItem', 'evoCondition', 'evos', 'eggGroups', 'canHatch', \
    'baseForme', 'genderRatio', 'weightkg', 'evoLevel']

with open('pokedex.js', 'r+') as f:
    for line in f:
        if not (any(ele in line for ele in notcare)):
            pokedex_js += line 

def insert (source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def javascript_dict_to_python(s): #TODO address boolean format, address errant quotes
    within_word = False
    s = s.replace('\"','')
    #find the location where single quotes should go
    single_quote_i = [] 
    for i in range(0,len(s)-1): 
        if s[i+1].isalpha() and (not within_word):
            single_quote_i.append(i+1)
            within_word = not within_word
        elif (not s[i+1].isalpha()) and within_word:
            single_quote_i.append(i+1)
            within_word = not within_word
    for i in reversed(single_quote_i): s = insert(s, '\'', i)
    
    quotes = find(s, '\'')
    remove_space_i = []
    for i in range(len(quotes)-1):
        if (s[quotes[i]+1:quotes[i+1]] == ' '):
            remove_space_i.append([quotes[i],quotes[i+1]])
    for rm in reversed(remove_space_i):
        s = f"{s[:rm[0]]} {s[rm[1]+1:]}"
    return s
    
js_dex = '{' + javascript_dict_to_python(pokedex_js.split('{',1)[1])
js_dex = js_dex.replace("'Farfetch'''d'","\"Farfetch'd\"")
js_dex = js_dex.replace("'Mr'. 'Mime'", "'Mr. Mime'")
js_dex = js_dex.replace("'porygon'2", "'porygon2'")
js_dex = js_dex.replace("'Porygon'2","'Porygon2'")
js_dex = js_dex.replace("'-'",'-')
js_dex = js_dex.replace("'Mime Jr'.","'Mime Jr.'")
js_dex = js_dex.replace("'Flabe'\\'u'0301'be'\\'u'0301","'Flabe\u0301be\u0301'")
js_dex = js_dex.replace("'zygarde'10","'zygarde10'")
js_dex = js_dex.replace("'Zygarde'-10%","'Zygarde-10%'")
js_dex = js_dex.replace("10%,","'10%',")
js_dex = js_dex.replace("{0:","{'0':")
js_dex = js_dex.replace("'Oricorio-Pa'''u'", "\"Oricorio-Pa'u\"")
js_dex = js_dex.replace("'Pa'''u'", "\"Pa'u\"")
js_dex = js_dex.replace("'Type': 'Null'", "'Type: Null'")
js_dex = js_dex.replace("'Missingno'.","'Missingno.'")
js_dex = js_dex.replace("'abilities': {'0': }","'abilities': {'0': \"\"}")
# js_dex = js_dex[:js_dex.index(";")]

pokedex = {}
exec('pokedex = ' + js_dex)

form_problems = []
for pokedex_entry in pokedex.values():
    if('otherForms' in pokedex_entry.keys()):
        for forme in pokedex_entry['otherForms']:
            if(forme not in pokedex.keys()):
                form_problems.append({forme:pokedex_entry})

for entry in form_problems:
    pokedex.update(entry)

js_dex = str(pokedex)

f = open('pokedex_dict.txt', 'w+')
f.write(js_dex)
f.close
kyk = 0
dicc = exec("kyk = " + js_dex)
