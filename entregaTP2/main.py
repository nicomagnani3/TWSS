import bs4 
import requests
import json
import html



if __name__ == "__main__":

    page= requests.get("https://www.imdb.com/title/tt1877830/?ref_=fn_al_tt_1").text
    soup= bs4.BeautifulSoup(page,"html.parser")  
    jsonPage = soup.find('script', {'type':'application/ld+json'}).contents
    json_object = json.loads(jsonPage[0]) 
    json_object=json.dumps(json_object, indent=4, ensure_ascii=False)
    

    pageRotten= requests.get("https://www.rottentomatoes.com/m/the_batman").text
    soupRotten= bs4.BeautifulSoup(pageRotten,"html.parser")  
    jsonPageRotten = soup.find('script', {'type':'application/ld+json'}).contents
    json_object = json.loads(jsonPageRotten[0]) 
    json_object=json.dumps(json_object, indent=4, ensure_ascii=False)

    pageMeta= requests.get("https://www.metacritic.com/movie/the-batman").text
    soupMeta= bs4.BeautifulSoup(pageMeta,"html.parser")  
    jsonPageMeta = soupMeta.find('script', {'type':'application/ld+json'}).contents
    json_object = json.loads(jsonPageMeta[0]) 
    json_object=json.dumps(json_object, indent=4, ensure_ascii=False)
    print(json_object)


