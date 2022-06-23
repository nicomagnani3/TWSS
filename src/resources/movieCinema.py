import bs4 
import requests
import json
import html

class MovieCinema():


   def getMoviesCinema():
      pageHTMLCartelera= requests.get("http://www.cinemalaplata.com/cartelera.aspx").text
      soup= bs4.BeautifulSoup(pageHTMLCartelera,"html.parser")
      movies = soup.find_all('div',attrs={"class":"page-container singlepost"})
      data=[] 
      for movie in movies:              
         details=MovieCinema.getDetailsMovieCinema(movie, movie.find('a').string)   
         data.append(details)
      

      data= {"peliculas": [data]}
      with open("Entrega/data/moviesCinema.json", "w", encoding='utf8') as outfile:
                     json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True)
      return json.dumps(data, indent=4, ensure_ascii=False) 

   
  

   def getSalaAndHoursMovieCinema(movieSoup):    
      horarios=movieSoup.find_all('div',attrs={"class":"col-2"})  
      detailsFunction=[]      
      for horario in horarios:         
         nameCine =horario.find('span').text            
         funcion = horario.find('p').text   
         funcion=html.unescape(funcion.replace("\n", " "))    
         detailsFunction.append({"cine":nameCine,"horarios":funcion})
       
      
      return detailsFunction
  
   
  
   def getDetailsMovieCinema(movie,nombreMovie):
        link = movie.find('a').get('href')
        fullLink = "http://www.cinemalaplata.com/" + link
        movieHTML= requests.get(fullLink).text
        movieSoup= bs4.BeautifulSoup(movieHTML,"html.parser")
        detalleMovie=movieSoup.find_all('div',attrs={"class":"dropcap6"})

        for detail in detalleMovie:
            
            nombre= detail.find('h4').string
            nombre= nombre.strip()
            if (nombre == 'Género'):
               genero= detail.find('span').string       
            if (nombre == 'Origen'):
               origen= detail.find('span').string
            if (nombre == 'Duracion'):
               duracion= detail.find('span').string
            if (nombre == 'Actores'):
               actores= detail.find('span').string
            if (nombre == 'Director'):
               director= detail.find('span').string

        horario = MovieCinema.getSalaAndHoursMovieCinema(movieSoup)    
        dictionary = {
               "titulo":nombreMovie,
               "genero" :genero,
               "origen" :origen,  
               "duracion" :duracion,   
               "actores" :actores, 
               "directores":director,
               "funciones":horario 
            }
        return dictionary

            
          

        