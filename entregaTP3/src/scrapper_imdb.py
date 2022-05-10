import json
from bs4 import BeautifulSoup
import requests
import bs4


def recolectar_imdb():
            jsonMovies = []
            page = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm').text
            soup = bs4.BeautifulSoup(page, "html.parser")
            movies = soup.find_all('td',attrs={"class":"titleColumn"})
            movies
            for movie in movies:
                link = movie.find('a').get('href')
                fullLink = "https://www.imdb.com/" + link
                movieHTML= requests.get(fullLink).text
                movieSoup= bs4.BeautifulSoup(movieHTML,"html.parser")
                jsonPage = movieSoup.find(
                    'script', {'type': 'application/ld+json'}).contents
                json_object = json.loads("".join(jsonPage), strict=False)
                jsonMovies.append(json_object)

            with open("entregaTP3/data/imdb.json", "w", encoding='utf8') as outfile:
                outfile.write(json.dumps(jsonMovies, indent=4, ensure_ascii=False))
            return jsonMovies  