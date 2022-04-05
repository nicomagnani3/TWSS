import bs4 
import requests
import json

class MovieCinpolis():

    def getMoviesCinepolis():
        
      pageHtmlCinepolis= requests.get("https://www.cinepolis.com.ar/proximos-estrenos").text       
      movieSoup= bs4.BeautifulSoup(pageHtmlCinepolis,"html.parser")
      movies = movieSoup.find('main',attrs={"class":"flex-fill"})     
      movies = movies.find_all('div',attrs={"class":"slide-call p-3"})
      data=[] 
      for movie in movies:        
        details = MovieCinpolis.getDetailsMovie(movie)
        data.append(details)
      return json.dumps(data, indent=4, ensure_ascii=False) 

       
        
    def getDetailsMovie(movie):
        urlDetailMovie=   movie.find('a', href=True)      
        detailMovie= requests.get(urlDetailMovie['href']).text
        movieDetailSoup= bs4.BeautifulSoup(detailMovie,"html.parser")
        detailsComplete = movieDetailSoup.find_all('div',attrs={"class":"col mt-3 mt-md-0"})        
        if (len(detailsComplete) == 0):
            detailsComplete = movieDetailSoup.find_all('div',attrs={"class":"col"})
        
        for detail in detailsComplete:                  
            detail = detail.find_all("strong")
            detailsDictionary = MovieCinpolis.getDictionaryMovie(detail)
            return detailsDictionary
            
        

    def getDictionaryMovie(details):        
        for detail in details:
            nombre= detail.next
            if (nombre == 'Género'):
               genero= detail.next_sibling.strip().replace(":", "")
            if (nombre == 'Título Original'):
               nombreMovie= detail.next_sibling.strip().replace(":", "")
            if (nombre == 'Origen'):
               origen= detail.next_sibling.strip().replace(":", "")
            if (nombre == 'Director'):
               duracion= detail.next_sibling.strip().replace(":", "")
            if (nombre == 'Actores'):
               actores=detail.next_sibling.strip().replace(":", "")
            if (nombre == 'Director'):
               director= detail.next_sibling.strip().replace(":", "")

        dictionary = {
               "titulo":nombreMovie,
               "genero" :genero,
               "origen" :origen,  
               "duracion" :duracion,   
               "actores" :actores, 
               "director":director,
            }
        return dictionary

            
            
 

