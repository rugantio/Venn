# Introduction
This project is intended to provide an innovative visualization for differential analysis of profiles for the [facebook tracking exposed](https://facebook.tracking.exposed/) project. Fbtrex keeps information in a mongo database. Content of posts is stored in the form of JSON files. I use python scripts to process this data and produce useful insight for the study.

## How it works
All the profiles are counted and stored in a list; this list is then used to construct all the possible combinations of the profiles, taken 3 at a time to make venn diagrams. Every post is tagged with a list of labels provided by [Dandelion](https://dandelion.eu/), and associated to a profile.
Venn.py counts the words (labels) of every profile and uses venn3 function from matplotlib to produce all the possible venn diagrams, with the number of common words used as data.
Vennwords.py does the same thing but instead of providing the number of the words, supplies the words themselves, generating a wordcloud for every profile and then intersecting with the ones of other profiles.

## Usage
In this project I use Python3; if you are using Python2 it will probably not work, is up to you to figure out how to fix the code. To use this tool some dependencies are needed, they can be installed via standard python library manager, pip or pip3, or via git.
* Standard python science libs: matplotlib, numpy
* matplotlib-venn
* matplotlib-venn-wordcloud

For matplotlib-venn-wordcloud I suggest to install [my fork](https://github.com/rugantio/matplotlib_venn_wordcloud), because otherwise the venn circles inclosed in the diagrams will be adjust to the size of the words.

```
$ python venn.py NAMEOFJSON.json
$ python vennwords.py NAMEOFJSON.json
```
The pictures generated will be found in a new directory named "images". 
