import bs4 
import requests

class Movie():

   def getNameMovieCinema(movie):
      return movie.find('a').string
   
   def getSalaAndHoursMovieCinema(movie):
        link = movie.find('a').get('href')
        fullLink = "http://www.cinemalaplata.com/" + link
        movieHTML= requests.get(fullLink).text
        movieSoup= bs4.BeautifulSoup(movieHTML,"html.parser")
        horarios=movieSoup.find_all('div',attrs={"class":"col-2"})
        for horario in horarios:            
            print(horario)
                  


   def getDetailsMovieCinema(movie):
        link = movie.find('a').get('href')
        fullLink = "http://www.cinemalaplata.com/" + link
        movieHTML= requests.get(fullLink).text
        movieSoup= bs4.BeautifulSoup(movieHTML,"html.parser")
        return movieSoup.find_all('div',attrs={"class":"dropcap6"})

        