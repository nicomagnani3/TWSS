import bs4
import requests
import json
import html
import datetime

def getMoviesCinema():
    pageHTMLCartelera = requests.get(
        "http://www.cinemalaplata.com/cartelera.aspx").text
    soup = bs4.BeautifulSoup(pageHTMLCartelera, "html.parser")
    movies = soup.find_all('div', attrs={"class": "page-container singlepost"})
    data = []
    for movie in movies:
        details = getDetailsMovieCinema(movie, movie.find('a').string)
        data.append(details)

    with open("entregaTP3/data/cinemalp.json", "w", encoding='utf8') as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))
    return data

"revisar salto de linea"
def getSalaAndHoursMovieCinema(movieSoup):
    horarios = movieSoup.find_all('div', attrs={"class": "col-2"})
    detailsFunction = []
    for horario in horarios:  
        nameCine = horario.find('span').text
        nameCine=nameCine.split(" - ")
        nameCine
        funcion = horario.find('p').text
        print(funcion)
        funcion = html.unescape(funcion.replace("\n", " "))
        print(funcion)
        funcion=funcion.split(": ")
        print(funcion)
        funcion=funcion[1].strip()
        print(funcion)
        formato= nameCine[1].strip()
        detailsFunction.append(jsonScreeningEvent(nameCine[0], funcion, formato))  
          
    return detailsFunction    


def jsonScreeningEvent(name,funcion,formato):
    dia=datetime.date.today() + datetime.timedelta(days=1)
    return {
            '@type': 'ScreeningEvent',
            'location': jsonMovieTheater(name),
            'doorTime': f"{dia} {funcion}",
            'videoFormat': formato.strip().lower(),
        }

def jsonMovieTheater(name):
    return {
            '@type': 'MovieTheater',
            'name': name,
    }



def getDetailsMovieCinema(movie, nombreMovie):
    link = movie.find('a').get('href')
    fullLink = "http://www.cinemalaplata.com/" + link
    movieHTML = requests.get(fullLink).text
    movieSoup = bs4.BeautifulSoup(movieHTML, "html.parser")  
    horario = getSalaAndHoursMovieCinema(movieSoup)    
    dictionary = {
        "@type": "Movie",
        "name": nombreMovie,      
        "events": horario
    }
    return dictionary
