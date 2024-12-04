import streamlit as st
import http.client
import json
import requests
from bs4 import BeautifulSoup

# Configuration de l'API
API_HOST = "free-api-live-football-data.p.rapidapi.com"
API_KEY = "3c99262600msh5da2d3d13033579p1c677ejsnc94020f9ff0e"

# Fonction pour récupérer les actualités d'une équipe
def fetch_team_news():
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    conn.request("GET", "/football-get-team-news?teamid=8650&page=1", headers=headers)
    res = conn.getresponse()
    if res.status != 200:
        st.error(f"Erreur lors de la récupération des données : {res.status} {res.reason}")
        return None
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Fonction pour récupérer le contenu d'un article
def fetch_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire le contenu de l'article
        # Cela dépend de la structure du site. Par exemple :
        article_content = soup.find_all('p')  # Trouve tous les paragraphes
        text_content = ' '.join([p.get_text() for p in article_content])
        return text_content
    except Exception as e:
        st.error(f"Erreur lors de la récupération du contenu : {e}")
        return "Impossible de récupérer le contenu de cet article."

# Interface Streamlit
st.title("Actualités de l'équipe : Liverpool")

# Appel API pour récupérer les actualités de l'équipe
news_data = fetch_team_news()
articles_dict = []

if news_data and "response" in news_data and "news" in news_data["response"]:
    news_list = news_data["response"]["news"]

    # Afficher les actualités
    for news in news_list:
        if not "90min" in news.get('sourceStr', '').lower():
            st.image(news["imageUrl"], use_container_width=True)  # Affiche l'image
            st.subheader(news["title"])  # Titre de l'article
            st.write(f"Source: {news.get('sourceStr', 'Non spécifiée')}")
            st.write(f"Date: {news['gmtTime']}")

            # Gérer les URLs : si l'URL est complète ou partielle
            if news['page']['url'].startswith("http"):
                full_url = news['page']['url']
            else:
                if "fotmob" in news.get('sourceStr', '').lower():
                    base_url = "fotmob.com"
                else:
                    base_url = "unknown-source.com"
                full_url = f"https://{base_url}{news['page']['url']}"


            

            # Afficher le lien pour lire l'article
            st.write(f"[Lire l'article complet]({full_url})", unsafe_allow_html=True)

            # Récupérer et afficher le contenu de l'article
            st.write("**Contenu de l'article :**")
            article_content = fetch_article_content(full_url)
            st.write(article_content[:500]+"...")  # Limiter l'affichage à 500 caractères
            st.write("---")  # Ligne de séparation
            
            
            # Ajouter les données dans un dictionnaire
            article_data = {
                "title": news["title"],
                "source": news.get('sourceStr', 'Non spécifiée'),
                "date": news["gmtTime"],
                "url": full_url,
                "content": article_content
            }
            articles_dict.append(article_data)
    #print(articles_dict)
else:
    st.write("Aucune actualité disponible pour l'équipe sélectionnée.")
