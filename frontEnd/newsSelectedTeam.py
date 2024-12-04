import streamlit as st
import http.client
import json

# Configuration de l'API
API_HOST = "free-api-live-football-data.p.rapidapi.com"
API_KEY = "3c99262600msh5da2d3d13033579p1c677ejsnc94020f9ff0e"

# Fonction pour récupérer les équipes correspondant à la recherche
def get_teams(search_term):
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    conn.request("GET", f"/football-teams-search?search={search_term}", headers=headers)
    res = conn.getresponse()
    if res.status != 200:
        st.error(f"Erreur lors de la récupération des équipes : {res.status} {res.reason}")
        return []
    data = res.read()
    try:
        decoded_data = json.loads(data.decode("utf-8"))
        suggestions = decoded_data.get("response", {}).get("suggestions", [])
        return suggestions
    except json.JSONDecodeError as e:
        st.error(f"Erreur de décodage JSON : {e}")
        return []

# Fonction pour récupérer les actualités d'une équipe
def fetch_team_news(team_id):
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    conn.request("GET", f"/football-get-team-news?teamid={team_id}&page=1", headers=headers)
    res = conn.getresponse()
    if res.status != 200:
        st.error(f"Erreur lors de la récupération des actualités : {res.status} {res.reason}")
        return None
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Interface Streamlit
st.title("Actualités footballistiques")

# Étape 1 : Récupération des équipes
teams = get_teams("m")  # Fetch teams with "m" in their name
if not teams:
    st.write("Aucune équipe disponible.")
else:
    # Construire les options pour le menu déroulant
    team_options = {f"{team['name']} ({team['leagueName']})": team["id"] for team in teams}
    selected_team = st.selectbox("Sélectionnez une équipe :", list(team_options.keys()))

    if selected_team:
        team_id = team_options[selected_team]

        # Étape 2 : Récupération et affichage des actualités
        st.subheader(f"Actualités pour l'équipe : {selected_team}")
        news_data = fetch_team_news(team_id)

        if news_data and "response" in news_data and "news" in news_data["response"]:
            news_list = news_data["response"]["news"]

            # Afficher les actualités
            for news in news_list:
                st.image(news.get("imageUrl", ""), use_column_width=True)  # Affiche l'image si disponible
                st.subheader(news["title"])  # Titre de l'article
                st.write(f"Source: {news.get('sourceStr', 'Non spécifiée')}")
                st.write(f"Date: {news['gmtTime']}")

                # Lien vers l'article complet
                full_url = news['page']['url']
                if not full_url.startswith("http"):
                    full_url = f"https://unknown-source.com{full_url}"
                st.write(f"[Lire l'article complet]({full_url})", unsafe_allow_html=True)
                st.write("---")
        else:
            st.write("Aucune actualité disponible pour l'équipe sélectionnée.")
