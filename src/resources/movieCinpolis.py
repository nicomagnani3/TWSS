import bs4
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from resources.funcion import Funcion
from selenium.common.exceptions import TimeoutException
from time import sleep


from bs4 import BeautifulSoup


class MovieCinpolis():

 def buscarCinepolis():
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.get("https://www.cinepolis.com.ar/")
        lisMovies = []
        movies = [p.get_attribute("href") for p in driver.execute_script(
            'return document.querySelectorAll(".movie-grid .movie-thumb")')]
        for urlMovie in movies:          
                urlMovie
                movie = getDetailsMovieCinepolis(urlMovie,driver)
                lisMovies.append(movie)
                print(movie)
              

        data= {"peliculas": [JsonMovie(movie)for movie in lisMovies]}
        data
        with open("Entrega/data/moviesCinepolis.json", "w", encoding='utf8') as outfile:
                     json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True)
        return lisMovies

def JsonMovie(movie):   
 
    return {
            "titulo": movie["titulo"],
            "origen": movie["origen"],
            "actores":movie["actores"],
            "directores":movie["director"],
            "genero": movie["genero"],
            "funciones": [funcion.toJSON() for funcion in movie["funciones"]]                    
        }

def getFuncion( idioma, horario, cine, formato, dia=None):
   dictionary = {
               "idioma":idioma, 
               "horario" :horario,
               "cine" :cine,  
               "formato" :formato,   
               "dia" :dia,
            }
   return dictionary

def getDetailsMovieCinepolis(url,driver):
    pelicula = requests.get(url).text
    pelicula = BeautifulSoup(pelicula, "html.parser")
    detalleMovie = pelicula.find("div", attrs={"id": "tecnicos"})
    infostr = []
    for detail in detalleMovie:
        detail
        x = detail.get_text().split("\n")
        for f in x:
            infostr.append(f)
    infostr = list(filter(lambda x: x.strip(), infostr))
    detalleMovieObject = {}
    for info in infostr:
        i = info.split(': ')
        detalleMovieObject[i[0]] = i[1] 
    movie = getMovie(detalleMovieObject,url,driver)    

    return movie

def getMovie(movie,url,driver):  
   duracion = None  
   check = 'Duraci??n' in movie 
   if check:
      duracion = movie['Duraci??n']

   driver.get(url)
   WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "showtimes-filter-component-dates"))
   )
   botones_dias =  driver.find_element_by_class_name('showtimes-filter-component-dates').find_elements(By.TAG_NAME, "button")
   funciones= []  
   botones_dias  
   for boton in botones_dias:
        dia= boton.get_attribute("value")
        boton.click()
        card_cine_todas= driver.find_elements(By.CLASS_NAME,("card"))
        for card_cine in card_cine_todas:
            nombre_cine = card_cine.text
            tipo_funcion_todas = card_cine.find_elements(By.CLASS_NAME,("movie-showtimes-component-combination"))
            tipo_funcion_todas
            for tipo_funcion in tipo_funcion_todas:
                funciones.extend(cargarFuncionesCinepolis(nombre_cine, tipo_funcion, dia,driver))

   isActors = 'Actores' in movie 
   isDirector = 'Director' in movie 
   isOrigen = 'Origen' in movie 
   isGenero = 'G??nero' in movie 
   dictionary = {
               "titulo":movie['T??tulo Original'], 
               "genero" :movie['G??nero'] if isGenero  else '-',
               "origen" :movie['Origen'] if isOrigen  else '-',
               "duracion" :duracion,   
               "actores" :  movie['Actores'] if isActors  else '-',
               "director":movie['Director'] if isDirector  else '-', 
               "funciones":funciones

            }
   return dictionary


def cargarFuncionesCinepolis(nombre_cine, tipo_funcion, dia,driver):
    funciones = []
    idioma = tipo_funcion.find_element(By.TAG_NAME, "small").get_attribute("textContent")    
    for horario in tipo_funcion.find_elements(By.CLASS_NAME, "btn-detail-showtime"):
        try:
            driver.set_page_load_timeout(10)
            funciones.append(
                Funcion(
                    idioma.split("???")[2], 
                    horario.get_attribute("textContent"), 
                    nombre_cine,
                    " ".join(" ".join(idioma.split("???")[0:2]).split()),
                    dia
                )
            )
            driver.set_page_load_timeout(10)

        except TimeoutException as ex:
                print("failed")
                continue
        
    funciones
    return funciones





