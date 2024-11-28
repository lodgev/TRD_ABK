import streamlit as st
import http.client
import json

# Configuration de l'API
API_HOST = "free-api-live-football-data.p.rapidapi.com"
API_KEY = "3c99262600msh5da2d3d13033579p1c677ejsnc94020f9ff0e"

# Fonction pour récupérer les données de l'API
def fetch_trending_news():
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    conn.request("GET", "/football-get-trendingnews", headers=headers)
    res = conn.getresponse()
    if res.status != 200:
        st.error(f"Erreur lors de la récupération des données : {res.status} {res.reason}")
        return None
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Interface Streamlit
st.title("Actualités de Football en Direct")

# Appel API pour récupérer les actualités tendance
news_data = fetch_trending_news()

if news_data and "response" in news_data and "news" in news_data["response"]:
    news_list = news_data["response"]["news"]

    # Afficher les actualités
    for news in news_list:
        st.image(news["imageUrl"], use_column_width=True)  # Affiche l'image
        st.subheader(news["title"])  # Titre de l'article
        st.write(f"Source: {news.get('sourceStr', 'Non spécifiée')}")
        st.write(f"Date: {news['gmtTime']}")
        st.write(f"[Lire l'article complet](https://{API_HOST}{news['page']['url']})", unsafe_allow_html=True)
        st.write("---")  # Ligne de séparation
else:
    st.write("Aucune actualité disponible pour le moment.")
