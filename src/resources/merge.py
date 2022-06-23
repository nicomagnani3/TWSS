import requests
import json
import html
import copy
import collections

class Merge():

    def mergeMovies():     
        with open('Entrega/data/moviesCinema.json', 'r', encoding="utf8") as openfile:  
            moviesCinema= json.load(openfile)
        with open('Entrega/data/moviesCinepolis.json', 'r', encoding="utf8") as openfile:  
            moviesCinepolis= json.load(openfile)
       
        merge=Merge.deepupdate(moviesCinepolis,moviesCinema)
        merge
        with open("Entrega/data/merge.json", "w", encoding='utf8') as outfile:
                     json.dump(merge, outfile, ensure_ascii=False, indent=4, sort_keys=True)
        merge

    def deepupdate(dict1, dict2):
        return dict(list(dict2.items()) + list(dict1.items()))
            
           
       