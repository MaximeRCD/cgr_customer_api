from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from itertools import product
import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Content-Type": 'application/json; charset=utf-8'
} # Ceci est important pour éviter les blocages

def create_research_triplets(client_data):
    localisation = client_data['criteres']['localisation']
    code_postal = client_data['criteres']['code_postal']
    type_bien = client_data['criteres']['type_bien']

    # Vérification si les longueurs de localisation et code_postal sont identiques
    if len(localisation) != len(code_postal):
        print("Les listes localisation et code_postal doivent avoir la même longueur.")
    else:
        # Création des triplets possibles
        triplets = list(product(type_bien, zip(localisation, code_postal)))
        triplets = [(type_bien, local, zipcode) for type_bien, (local, zipcode) in triplets]

    return triplets

def create_urls(client_data):
    urls = []
    root_url = "https://www.iadfrance.fr"
    triplets = create_research_triplets(client_data)
    for triplet in triplets:
        localisation = triplet[1]
        code_postal = triplet[2]
        type_bien = triplet[0]
        max_price = client_data['criteres']['max_price']
        min_price = client_data['criteres']['min_price']
        max_surface = client_data['criteres']['max_surface']
        min_surface = client_data['criteres']['min_surface']
        url = url = f"{root_url}/annonces/{localisation}-{code_postal}/vente/{type_bien}?price_max={max_price}&price_min={min_price}&surface_max={max_surface}&surface_min={min_surface}"
        urls.append(url)
    return urls

def make_research(client_data, urls):
    matches = []
    root_url = "https://www.iadfrance.fr"

    bien_information = {
        "user_id":client_data['_id'],
        "type":"",
        "surface":"",
        "nb_piece":"",
        "localisation":"",
        "prix":"",
        "annonce":"",
        "annonce_id":"",
        "description":"",
        "image":""
    }
    for url in urls :
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            results_sections = soup.find(id='results-list')
            photos = results_sections.find_all('picture')
            photos = list(map(lambda x: root_url+x.select('picture source')[0]["srcset"].split(',')[0], photos))
            results_list = soup.find_all(class_='i-card--content')
            for idx, listing in enumerate(results_list[:-1]):
                try : 
                    title_div = listing.find(class_='i-card--title')
                    bien_information["annonce"] = root_url+title_div.find('a').get('href')
                    bien_information["annonce_id"] = bien_information["annonce"].split("/")[-1]
                    bien_information["image"] = photos[idx]
                    title = title_div.text
                    title_info = title.strip().split(" ")          
                    bien_information["type"]=title_info[0]
                    bien_information["surface"]=" ".join(title_info[4:6])
                    bien_information["nb_piece"]=" ".join(title_info[1:3])
                    bien_information["localisation"]=" ".join(title_info[title_info.index('à')+1:])
                    bien_information["prix"]=" ".join(listing.find(class_='i-card--informations').text.strip().split(" ")[:-1])
                    bien_information["description"]=listing.find(class_='i-card--description').text
                    matches.append(bien_information)
                    bien_information = {
                        "user_id":client_data['_id'],
                        "type":"",
                        "surface":"",
                        "nb_piece":"",
                        "localisation":"",
                        "prix":"",
                        "annonce":"",
                        "description":""
                    }
                except Exception as e:
                    print(e)
                    
            else:
                print("Erreur:", response.status_code)
    return matches

def store_an_delete_researches(all_researchs):
    all_added_or_updated_researches = []
    for research in all_researchs[:2]:
        try:
            insert = requests.post('http://localhost:8000/research/', data=json.dumps(research, ensure_ascii=False).encode("UTF-8"), headers=HEADERS)
            if insert.status_code == 200:
                print(f"new research added")
                all_added_or_updated_researches.append(insert.json()["_id"])
            else:
                client_id = research['user_id']
                annonce_id = research['annonce_id']
                update = requests.put(f'http://localhost:8000/research/?client_id={client_id}&annonce_id={annonce_id}', data=json.dumps(research, ensure_ascii=False).encode("UTF-8"), headers=HEADERS)
                if update.status_code == 200:
                    print(f" research updated")
                    all_added_or_updated_researches.append(update.json()["_id"])
        except Exception as e:
            print("Erreur:", e)
            
    try:
        all_clients_found = list(map(lambda x: x["_id"], requests.get(f'http://localhost:8000/research/{client_id}').json()))
        difference = list(set(all_clients_found)-set(all_added_or_updated_researches))
        print(f"diff: {difference}")
        for _id in difference:
            deleted = requests.delete(f"http://localhost:8000/research/?research_id={_id}")
            if deleted.status_code == 200:
                print(f"Old research deleted")
    except Exception as e:
        print(e)

# Define a function you want to schedule
def my_scheduled_function():
    clients = requests.get("http://localhost:8000/clients").json()
    for client in clients :
        print(f"############################ Start Searching Houses for {client['name']} ####################################")
        client_urls = create_urls(client_data=client)
        all_researches = make_research(client, client_urls)
        store_an_delete_researches(all_researches)
        print(f"############################ End of research for {client['name']} ##########################################")



if __name__=="__main__":
    # Initialize the scheduler with the background scheduler
    scheduler = BackgroundScheduler(timezone=utc)

    # Add the scheduled function to the scheduler with the desired interval (seconds)
    scheduler.add_job(my_scheduled_function, "interval", seconds=600)

    # Start the scheduler
    scheduler.start()