from tokenize import String
import bs4 
import requests
from movie import Movie
import json


if __name__ == "__main__":

    print(Movie.getMoviesCinema())
    pageHTMLCartelera= requests.get("https://www.cinepolis.com.ar/").text
    soup= bs4.BeautifulSoup(pageHTMLCartelera,"lxml")
    movies = soup.find('section',attrs={"class":"featured-movies-section"})
    movies
    print(movies)
    
    


    
    
    
  

    
        



    
