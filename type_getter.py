import json
import pandas as pd

showdata = pd.read_csv('data.csv')

pokedex_js = ''

with open('pokedex.js', 'r+') as f:
    pokedex_js = f.read()

def insert (source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def javascript_dict_to_python(s): #TODO address boolean format, address errant quotes
    within_word = False
    s = s.replace('\"','')
    
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
    
print(javascript_dict_to_python(pokedex_js)) 

# f = open('pokedex_dict.txt', 'w+')
# f.write(js_dex)
# f.close
