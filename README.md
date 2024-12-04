# RTD_ABK


### Comment l'implémenter ?

1. **Installer les dépendances** :
   - Assurez-vous d'avoir **Python** installé.
   - Installez **Streamlit** :
     ```bash
     pip install streamlit
     ```

2. **Exécuter l'application** :
   - Placez le code ci-dessus dans un fichier `app.py`.
   - Lancez le serveur Streamlit avec :
     ```bash
     streamlit run app.py
     ```

3. **Configurer votre clé API** :
   - Remplacez `"3c99262600msh5da2d3d13033579p1c677ejsnc94020f9ff0e"` par votre propre clé API.

4. **Naviguer sur l'interface** :
   - Ouvrez le lien fourni dans le terminal (par défaut, `http://localhost:8501`).
   - Utilisez les options pour visualiser les actualités, transferts, ou autres données.

---

### Explication du fonctionnement
- **Récupération des données :**
  La fonction `fetch_data` envoie des requêtes GET à l'API en utilisant le module `http.client`.
- **Affichage interactif :**
  - Les utilisateurs interagissent avec la barre latérale et les boutons pour sélectionner les options souhaitées.
  - Les données récupérées sont affichées dans un format lisible.


---

- **installation beautiful soup**
Getting the content of the article from the url recuire the package beautiful soup. You need to run `pip install beautifulsoup4` in your terminal.
