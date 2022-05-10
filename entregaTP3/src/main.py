import json
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD
from datetime import datetime
from scapper_cinema import getMoviesCinema
from scrapper_imdb import recolectar_imdb

BASE_URL = Namespace("http://www.semanticweb.org/")
BASE_SCHEMAORG_URL = Namespace("https://schema.org/")
g = Graph()
g.bind("schema", BASE_SCHEMAORG_URL)
g.bind("sw", BASE_URL)


def posicion(node_type: str, url):
    return len(list(g.triples((None, RDF.type, url[node_type]))))

def addIndividual(tipo, text, url=BASE_URL):    
    for s, p, o in g.triples((None, RDFS.label, Literal(text))):
        return s

    urlTipo= url[tipo.lower()+str(posicion(tipo, url))]
    g.add((urlTipo, RDF.type, url[tipo]))
    g.add((urlTipo, RDFS.label, Literal(text)))
    g.add((urlTipo, BASE_SCHEMAORG_URL["name"], Literal(text)))
    return urlTipo 

def addActors(movie, actor):
    actor= addIndividual(
            actor.get("@type"),
            actor.get("name"),
            url= BASE_SCHEMAORG_URL
        )
    g.add((movie, BASE_SCHEMAORG_URL["actor"], actor))


def addRanting(movie, rating):
    rating_individual= BASE_URL["aggregateRating"+str(posicion("AggregateRating", url=BASE_SCHEMAORG_URL))]
    g.add((rating_individual, RDF.type, BASE_SCHEMAORG_URL["AggregateRating"]))
    if (rating is not None):
        g.add((rating_individual, BASE_SCHEMAORG_URL["ratingValue"], Literal(rating.get("ratingValue"), datatype=XSD.double)))
    g.add((movie, BASE_SCHEMAORG_URL["aggregateRating"], rating_individual))


def addImageSemanticWeb(imageurl):
    img_obj= BASE_URL["image"+str(posicion("ImageObject", url=BASE_SCHEMAORG_URL))]
    img_obj
    g.add((img_obj, RDF.type, BASE_SCHEMAORG_URL["ImageObject"]))
    g.add((img_obj, BASE_SCHEMAORG_URL["contentUrl"], Literal(imageurl)))
    return img_obj

def addMovies(movie):
    pelicula= addIndividual(
        movie.get("@type"),
        movie.get("name"),
        url= BASE_SCHEMAORG_URL
    )        
    pelicula
    g.add((URIRef(pelicula), BASE_SCHEMAORG_URL["duration"], Literal(movie.get("duration"), datatype= XSD.duration))) 
    g.add((URIRef(pelicula), BASE_SCHEMAORG_URL["image"], addImageSemanticWeb(movie.get("image")))) 
    if (movie.get("datePublished") is not None):
         g.add((URIRef(pelicula), BASE_SCHEMAORG_URL["datePublished"], Literal(datetime.strptime(movie.get("datePublished"), '%Y-%m-%d').isoformat(), datatype=XSD.date))) 
    actor=[]
    genre=[]
    director=[]
    for actor in movie.get("actor"):
        actor= addIndividual(
            actor.get("@type"),
            actor.get("name"),
            url= BASE_SCHEMAORG_URL
        )
        g.add((URIRef(pelicula), BASE_SCHEMAORG_URL["actor"], actor))

    for genre in movie.get("genre"):
        g.add((URIRef(pelicula), BASE_SCHEMAORG_URL["genre"], Literal(genre)))
   
    for director in movie.get("director"):
        g.add((URIRef(pelicula), BASE_SCHEMAORG_URL["director"], addIndividual(
            director.get("@type"),
            director.get("name"),
            url= BASE_SCHEMAORG_URL
        )))   

    addRanting(URIRef(pelicula), movie.get("aggregateRating"))

def addFunciones(movie):

        peli = addIndividual("Movie", movie.get("name"), BASE_SCHEMAORG_URL)
        peli
        for funcion in movie.get("events"):
            urlSemanticWeb= BASE_URL["screeningEvent"+str(posicion("ScreeningEvent", url=BASE_SCHEMAORG_URL))]
            urlSemanticWeb
            funcion
            g.add((urlSemanticWeb, RDF.type, BASE_SCHEMAORG_URL["ScreeningEvent"]))
            g.add((urlSemanticWeb, BASE_SCHEMAORG_URL["videoFormat"], Literal(funcion.get("videoFormat")))) 
            g.add((urlSemanticWeb, BASE_SCHEMAORG_URL["doorTime"], Literal(funcion.get("doorTime")))) 
            g.add((urlSemanticWeb, BASE_SCHEMAORG_URL["workPresented"], peli)) 
            
            cine= funcion.get("location")
            cine_individual= addIndividual(
                cine.get("@type"),
                cine.get("name"),
                url= BASE_SCHEMAORG_URL)

            g.add((urlSemanticWeb, BASE_SCHEMAORG_URL["location"], cine_individual)) 
   
    
if __name__ == "__main__":
    #getMoviesCinema() 
    #recolectar_imdb()
    with open('entregaTP3/data/imdb.json', encoding='utf-8') as fh:
        json_peliculas = json.load(fh)

    with open('entregaTP3/data/cinemalp.json', encoding='utf-8') as fh:
        json_funciones = json.load(fh)

    g.parse("entregaTP3/data/movies.ttl", format='ttl', encoding="utf-8")

    for movie in json_peliculas:
        addMovies(movie)

    for movie in json_funciones:
        addFunciones(movie)


    g.serialize("entregaTP3/data/output.ttl", format="ttl", encoding="utf-8")