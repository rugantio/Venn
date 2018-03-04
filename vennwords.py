import codecs
import os
import sys
import itertools
import json 
import pprint
from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles, venn3_unweighted
from matplotlib_venn_wordcloud import venn3_wordcloud
from wordcloud import WordCloud
from numpy import log

if len(sys.argv) < 2:
    print('JSON required')
    print('Usage: \'python venn.py nameofjson.json\'')
    sys.exit()

with codecs.open(sys.argv[1],encoding='utf-8') as data_json:   # load the mongo json
    data = json.load(data_json)

profiles = [item['profile'] for item in data if 'profile' in item] # get all profiles
profiles = set(profiles)                                           # put them in a set
diz = {name: '' for name in profiles}                              # initialize a dict with profile names

for name in diz:                             # for every profile
    wordlist = []                 # create a set
    for item in data:                        # take every post
        if 'profile' in item:
            if name == item['profile']:      # get post with such profile name
                if 'labels' in item:
                    for parola in item['labels']:    # get all the words in that post
                        wordlist.append(parola)          # add words to wordset
        diz[name] = wordlist              # update dictionary values relative to such profile

frequencies = {}
for name in diz:
    for word in diz[name]:
        if word not in frequencies:
            frequencies[word] = 1
        else:
            frequencies[word] += 1

for word in frequencies:
    frequencies[word] = log(frequencies[word])

for x,y,z in itertools.combinations(profiles,3):
    setx = set(diz[x])
    sety = set(diz[y])
    setz = set(diz[z])    
    s = (setx, sety, setz)
    
    #Change color of each set
#    if(v.get_patch_by_id('100')):
#        v.get_patch_by_id('100').set_color('#ff0000')
#    if(v.get_patch_by_id('010')):
#        v.get_patch_by_id('010').set_color('#00ff00')
#    if(v.get_patch_by_id('001')):  
#        v.get_patch_by_id('001').set_color('#0000ff')
#    if(v.get_patch_by_id('011')):
#        v.get_patch_by_id('011').set_color('#00ffff')
#    if(v.get_patch_by_id('101')):
#        v.get_patch_by_id('101').set_color('#ff00ff')
#    if(v.get_patch_by_id('111')):
#        v.get_patch_by_id('111').set_color('#ffffff')

    path = './images/'
    if not os.path.exists(path):
        os.makedirs(path)
        
    path1 = path + x + y + z
    #c = venn3_circles(s, linestyle='solid')     
     
## create venn sets filled with words  
    plt.rcParams["figure.figsize"] = (39,22)

    print('Generating Venn diagram with words for:', x, y, z)    
    v = venn3_wordcloud(s, set_labels=(x,y,z), alpha=0.7, word_to_frequency=frequencies, wordcloud_kwargs={'max_words':1800,'min_font_size':9,'width':3840,'height':2160})
    path3 = path1 + '_words'
    #plt.rcParams["figure.figsize"] = (20,11)
    plt.savefig(path3)
    plt.close()
