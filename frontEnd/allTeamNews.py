import http.client
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Configuration de l'API
API_HOST = "free-api-live-football-data.p.rapidapi.com"
API_KEY = "3c99262600msh5da2d3d13033579p1c677ejsnc94020f9ff0e"
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}

# Fonction pour appeler l'API et obtenir des données
def call_api(endpoint):
    conn = http.client.HTTPSConnection(API_HOST)
    conn.request("GET", endpoint, headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data)


# Fonction pour récupérer le contenu d'un article
def fetch_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire le contenu de l'article
        article_content = soup.find_all('p')  # Trouve tous les paragraphes
        text_content = ' '.join([p.get_text() for p in article_content])
        return text_content
    except Exception as e:
        return "Impossible de récupérer le contenu de cet article."

# Étape 1 : Récupérer les IDs des ligues
leagues_data = call_api("/football-get-all-leagues")
leagues = leagues_data.get("response", {}).get("leagues", [])

leagues_df = pd.DataFrame(leagues)
leagues_ids = leagues_df["id"]

# Étape 2 : Récupérer les IDs des équipes pour chaque ligue
teams_list = []
for league_id in leagues_ids:
    teams_data = call_api(f"/football-get-list-all-team?leagueid={league_id}")
    teams = teams_data.get("response", {}).get("list", [])
    for team in teams:
        team["league_id"] = league_id  # Associer l'équipe à sa ligue
        teams_list.append(team)

teams_df = pd.DataFrame(teams_list)
teams_ids = teams_df["id"]

# Étape 3 : Récupérer les actualités des équipes avec contenu des articles
news_list = []
for team_id in teams_ids:
    news_data = call_api(f"/football-get-team-news?teamid={team_id}&page=1")
    news = news_data.get("response", {}).get("news", [])
    for item in news:
        item["team_id"] = team_id  # Associer l'actualité à son équipe
        # Générer l'URL complète de l'article
        full_url = ""
        if item['page']['url'].startswith("http"):
            full_url = item['page']['url']
        else:
            if "fotmob" in item.get('sourceStr', '').lower():
                base_url = "fotmob.com"
            else:
                base_url = "unknown-source.com"
            full_url = f"https://{base_url}{item['page']['url']}"

        # Récupérer le contenu de l'article
        article_content = fetch_article_content(full_url)
        item["article_content"] = article_content  # Ajouter le contenu de l'article
        news_list.append(item)

news_df = pd.DataFrame(news_list)

# Résultats
print("Leagues DataFrame:")
print(leagues_df.head())

print("Teams DataFrame:")
print(teams_df.head())

print("News DataFrame:")
print(news_df.head())

# Sauvegarde des données dans des fichiers CSV
leagues_df.to_csv("leagues.csv", index=False)
teams_df.to_csv("teams.csv", index=False)
news_df.to_csv("news.csv", index=False)
