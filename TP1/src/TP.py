import urllib.parse
import urllib.request
import urllib.robotparser
import urllib
from bs4 import BeautifulSoup
import json

request_url = urllib.request.urlopen('https://ensai.fr/robots.txt')

def est_autorise(crawler: str, url: str):
    robot_parser = urllib.robotparser.RobotFileParser()
    return robot_parser.can_fetch('*', url=url)

def recuperer_titre_page(url: str):

    # On récupère le contenu de la page
    request_url = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(request_url, 'html.parser')

    return soup.title

def recuperer_liens_page(url: str):
    
    # On récupère le contenu de la page
    request_url = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(request_url, 'html.parser')

    # On extrait tous les liens (balise <a>)
    links = soup.find_all('a', href=True)

    return links

def recuperer_paragraphe_page(url: str):
    
    # On récupère le contenu de la page
    request_url = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(request_url, 'html.parser')

    # On extrait le premier lien (première balise <p>)
    first_paragraph = soup.find('p')

    return first_paragraph

def contient_token_product(url: str):

    parsed_url = urllib.parse.urlparse(url)
    
    return 'product' in parsed_url.path

def file_attente(list_url: list):

    list_triee = sorted(list_url, key=lambda x: contient_token_product(x), reverse=True)

    

def stocker_resultat(result: dict):
    
    try:
        with open("product.json", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(result)

    with open("product.json", 'w') as file:
        json.dump(data, file, indent=4)

data = {
    "nom": "Alice",
    "age": 30,
    "ville": "Paris"
}

stocker_resultat(data)
# print(est_autorise(crawler="*", url='https://web-scraping.dev/products'))
# print(recuperer_titre_page('https://web-scraping.dev/products'))
# print(recuperer_liens_page('https://web-scraping.dev/products'))
# print(recuperer_paragraphe_page('https://web-scraping.dev/products'))