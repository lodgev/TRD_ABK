import requests
import csv

# Définir les en-têtes et l'URL de l'API
url = 'https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-league'
headers = {
    'x-rapidapi-host': 'free-api-live-football-data.p.rapidapi.com',
    'x-rapidapi-key': '9db8926490msh1a59290023be149p1a041bjsnb95dac8acaf6'
}

# Paramètres de l'API
params = {
    'leagueid': '42'  # ID de la ligue
}

# Appel de l'API
response = requests.get(url, headers=headers, params=params)

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()

    # Extraire les données des matchs
    matches = data.get('response', {}).get('matches', [])

    # Sauvegarder les données dans un fichier CSV
    with open('matches.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Écrire l'en-tête du CSV
        writer.writerow(['Match ID', 'Home Team', 'Home Score', 'Away Team', 'Away Score', 'Score String', 'Date'])

        # Écrire les données des matchs
        for match in matches:
            match_id = match.get('id')
            home_team = match.get('home', {}).get('name')
            home_score = match.get('home', {}).get('score')
            away_team = match.get('away', {}).get('name')
            away_score = match.get('away', {}).get('score')
            score_str = match.get('status', {}).get('scoreStr')
            match_date = match.get('status', {}).get('utcTime')

            writer.writerow([match_id, home_team, home_score, away_team, away_score, score_str, match_date])

    print("Les données ont été enregistrées dans 'matches.csv'.")
else:
    print(f"Erreur lors de l'appel API : {response.status_code} - {response.text}")
