import bs4
import requests
import json
import simplejson 

class Movies():
    def __init__(self):
        self.urlMovies = [        
            {'url': 'https://www.rottentomatoes.com/m/the_batman', 'name': 'rottentomatoes'},
            {'url': 'https://www.imdb.com/title/tt1877830/?ref_=fn_al_tt_1',
             'name': 'imdb'},
            {'url': 'https://www.ecartelera.com/peliculas/the-batman/', 'name': 'ecartelera'}
            
        ]

    def save_movies_json(self):
        jsonMovies = []
        for movies in self.urlMovies:            
            page = requests.get(movies['url']).text
            soup = bs4.BeautifulSoup(page, "html.parser")
            jsonPage = soup.find(
                'script', {'type': 'application/ld+json'}).contents
            json_object = json.loads("".join(jsonPage), strict=False)
            jsonMovies.append(json_object)

        with open("entregaTP2/data/movies.json", "w", encoding='utf8') as outfile:
            outfile.write(json.dumps(jsonMovies, indent=4, ensure_ascii=False))
        return jsonMovies     
    

    def mergeMovies(self):
        with open('entregaTP2/data/movies.json', 'r', encoding="utf8") as openfile:  
            movies= json.load(openfile)
        Movies.armJsonMovies(movies)  

    def armJsonMovies(movies):
        actors=[]
        director=[]
        genre=[]
        duration=[]
        name=""
        for movie in movies:
            movie
            name=movie.get("name")
            actors.extend(Movies.getActors(movie))
            director.extend(Movies.getDirectors(movie))
            genre.extend(movie.get("genre"))
            movie
            duration.extend(Movies.getDuration(movie))
            duration
        Movies.jsonMovies(name,actors,director,genre,duration)

    def getDirectors(movie):
        arrayDirectors=[]
        directors=[]
        if movie.get("author") != None:
                directors.extend(movie.get("author"))            
        else:
                 directors.extend(movie.get("director")) 
        for director in directors:
            arrayDirectors.append(director.get("name"))
        
        return arrayDirectors
    
    def getActors(movie):
        arrayActorst=[]
        actores=[]
        if movie.get("actors") != None:
                actores.extend(movie.get("actors"))            
        else:
                 actores.extend(movie.get("actor")) 
        for actor in actores:
            arrayActorst.append(actor.get("name"))
        
        return arrayActorst


    def removeDuplicates(array):
        return set(array)
    
    def getDuration(movie):
        arrayDuration=[]
        if movie.get("duration") != None:
                arrayDuration.append(movie.get("duration"))           
        return arrayDuration

    def jsonMovies(name,actors,director,genre,duration):
        jsonMovie= {
            "@context": "http://schema.org",
            "@type": "Movie",
            "name": name,
            "actor":Movies.removeDuplicates(actors),
            "director":Movies.removeDuplicates(director),
            "genre":Movies.removeDuplicates(genre),
            "duration":Movies.removeDuplicates(duration),
        }   
        with open("entregaTP2/data/merge.json", "w", encoding='utf8') as outfile:
            outfile.write(simplejson.dumps(jsonMovie, indent=4, ensure_ascii=False,iterable_as_array=True))



