from tokenize import String
import bs4 
import requests
from movie import Movie


if __name__ == "__main__":

    pageHTMLCartelera= requests.get("http://www.cinemalaplata.com/cartelera.aspx").text
    soup= bs4.BeautifulSoup(pageHTMLCartelera,"html.parser")
    movies = soup.find_all('div',attrs={"class":"page-container singlepost"})
    names=[]
    for movie in movies:       
        name= Movie.getNameMovieCinema(movie) 
        names.append(name)
        if (name.replace(" ", "") == 'BATMAN'):
            
            Movie.getSalaAndHoursMovieCinema(movie)
        #movieDetails=Movie.getDetailsMovieCinema(movie)
        



    
