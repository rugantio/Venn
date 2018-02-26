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
    wordset = set()                          # create a set
    for item in data:                        # take every post
        if name == item['profile']:          # get post with such profile name
            for parola in item['labels']:    # get all the words in that post
                wordset.add(parola)          # add words to wordset
            diz[name] = wordset              # update dictionary values relative to such profile

for x,y,z in itertools.combinations(profiles,3):
    setx = set(diz[x])
    sety = set(diz[y])
    setz = set(diz[z])    
    s = (setx, sety, setz)
    
    print('Generating weighted Venn diagram for:', x, y, z)
    v = venn3(s, set_labels=(x,y,z), alpha=0.7)
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
    plt.savefig(path1 + '_weighted')
    plt.close() 
     
    print('Generating unweighted Venn diagram for:', x, y, z)
    v = venn3_unweighted(s, set_labels=(x,y,z), alpha=0.7)
    path2 = path1 + '_unweighted'
    plt.savefig(path2)
    plt.close()
     
## create venn sets filled with words  
    print('Generating Venn diagram with words for:', x, y, z)    
    v = venn3_wordcloud(s, set_labels=(x,y,z), alpha=0.7, wordcloud_kwargs={'max_words':5,'min_font_size':5})
    path3 = path1 + '_words'
    plt.savefig(path3)
    plt.close()



 ## for wordclouds I want also to count the frequencies so I use a list instead of a set   

for name in diz:                             # for every profile
    wordlist = []                          # create a set
    for item in data:                        # take every post
        if name == item['profile']:          # get post with such profile name
            for parola in item['labels']:    # get all the words in that post
                wordlist.append(parola)          # add words to wordset
            diz[name] = wordlist              # update dictionary values relative to such profile


for profile in profiles:
    words = diz[profile]
    path = './images/'
    path_txt = path + profile + '.txt'
    with codecs.open(path_txt,'w',encoding='utf-8') as wordlist:
        for word in words:
            wordlist.write('%s\n' % word)
    wordlist =  open(path_txt).read()
    wordcloud = WordCloud(width = 1024, height=768, max_words=500, margin=0).generate(wordlist)
    path3 = path + profile
    #plt.figure()
    print('Generating unweighted Venn diagram for:', profile)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(profile)
    plt.savefig(path3)
    plt.close()

