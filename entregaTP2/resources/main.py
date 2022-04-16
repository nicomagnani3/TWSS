import bs4 
import requests
import json
import html
from movies import Movies


if __name__ == "__main__":
    movies = Movies()    
    jsonMovie=movies.save_movies_json()
    mergeMovies=movies.mergeMovies()
    




