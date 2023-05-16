import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import requests

# Chargement en local en pikle
liste_films = pd.read_pickle("liste_films.pkl.gz")
df_genres2 = pd.read_pickle("df_genres2.pkl.gz")
df_films_note2 = pd.read_pickle("df_films_note2.pkl.gz")
df_annee = pd.read_pickle("df_annee.pkl.gz")
df_merge_finalML = pd.read_pickle("df_merge_finalML.pkl.gz")


# Configuration de la page
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    layout="wide",
    page_icon="🎞️")

# Titre
st.title("🎥Bienvenue dans notre humble application de recommandation de film")

# Header
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")
 
# listes
liste_films_deroulante_films = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])
liste_films_deroulante_genres = list(df_genres2["genres"])
liste_deroulante_acteur = list(df_films_note2["primaryName"])
liste_deroulante_annee = list(df_annee["startYear"])

# Subheader
st.subheader("Choisi ou tape ton film préféré 😎")

# Machine Learning Partie 1
# Récupération des noms des colonnes sans prendre const+primaryTitle+originalTitle+averageRating+numVotes+nconst+primaryProfession+knownForTitles
colonnes_ml = df_merge_finalML.columns[7:]

# Création de la variable X qui prends en variables explicatives toutes les colonnes numériques sauf (voir celles ci-dessus)
X = df_merge_finalML.loc[:, colonnes_ml]

# Initialisation du model avec 4 voisins
distanceKNN = NearestNeighbors(n_neighbors = 4, metric = "cosine", algorithm = "brute").fit(X)

# Bloc de mise en forme pour utilisateur
with st.form("form_1"):
            films = st.selectbox("Films : ", liste_films_deroulante_films)
            submit = st.form_submit_button(label="Submit")
if submit:      
# Machine Learning Partie 2
# Création liste de film
        liste_du_film = films

# Obtenir tous les renseignements du film
        df_film_choisi = df_merge_finalML[(df_merge_finalML["primaryTitle"] == films) | (df_merge_finalML["originalTitle"] == films)]

# On ne selectionne que les colonnes contenant des booleens sur la ligne du film choisi
        film_choisi = df_film_choisi.iloc[:, 7:]

# Création de la matrice pour rechercher les index des plus proches voisins
        matrice_des_plus_proches_voisins = distanceKNN.kneighbors(film_choisi)

# Création de la liste des suggestions à partir de la matrice
        suggestion = df_merge_finalML.iloc[matrice_des_plus_proches_voisins[1][0][1:], 0].values
        st.write("Je te propose :")

# Création d'une variable pour récupérer le tconst
        #tconst = df_merge_finalML.iloc[matrice_des_plus_proches_voisins[1][0][1:]]["tconst"].values
# Création d'une variable pour récupérer le nom du film
        nom_du_film = df_merge_finalML.loc[matrice_des_plus_proches_voisins[1][0][1:]]["primaryTitle"].values

# Api pour affiche de films
        url_api = "http://www.omdbapi.com/?i="
        key_api = "&apikey=ec8d0879"

# Création de colones
        col1 = st.columns(3)
     
# Boucle sur tconst et suggestion
        for film, nom, colonnes in zip(suggestion, nom_du_film, col1):
            with colonnes :
                url = url_api + str(film) + key_api
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    url_image = data['Poster']
                    st.image(url_image, width=200)
                except requests.exceptions.RequestException as e:
                    print("Une erreur est survenue lors de l'appel à l'API :", e)
                st.write(' - {}'.format(nom))


# Subheader
        st.subheader("Bon visionnage ! ❤")
