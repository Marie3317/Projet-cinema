import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import requests
from sklearn.preprocessing import MinMaxScaler

# Chargement en local en pikle
liste_films = pd.read_pickle("liste_films.pkl.gz")
df_genres2 = pd.read_pickle("df_genres2.pkl.gz")
df_films_note2 = pd.read_pickle("df_films_note2.pkl.gz")
df_annee = pd.read_pickle("df_annee.pkl.gz")
df2 = pd.read_pickle("df2.pkl.gz")
df2 = pd.read_pickle("df2.pkl.gz")


# Configuration de la page
st.set_page_config(
    page_title="Screeny-App",
    layout="wide",
    page_icon="🎞️")
#Mise en forme fond de page
page_bg_img = """
<style>
[data-testid = "stAppViewContainer"] {

background-color: #e5e5f7;
opacity: 0.8;
#background-image: radial-gradient(#444cf7 0.5px, #e5e5f7 0.5px);
background-size: 10px 10px;

}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html = True)

# Titre
st.title("Bienvenue dans notre humble application de recommandation de film 🎥")

# Header
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")
 
# listes
liste_films_deroulante_films = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])


# Api pour affiche de films
url_api = "http://www.omdbapi.com/?i="
key_api = "&apikey=ec8d0879"
url_imdb = "https://www.imdb.com/title/"

# Subheader
st.subheader("Choisis ou tape ton film préféré 😎")


# Machine Learning Partie 1

# Scaler : Uniformisation des données
scaling = MinMaxScaler()
df2[["averageRating", "numVotes", "runtimeMinutes", "startYear"]] = scaling.fit_transform(df2[["averageRating", "numVotes", "runtimeMinutes", "startYear"]])

# Récupération des noms des colonnes sans prendre const+primaryTitle+originalTitle+frenchTitle
colonnes_ml = df2.columns[4:]

# Création de la variable X qui prends en variables explicatives toutes les colonnes numériques sauf (voir celles ci-dessus)
X = df2.loc[:, colonnes_ml]

# Initialisation du model avec 4 voisins
distanceKNN = NearestNeighbors(n_neighbors = 4, metric = "cosine", algorithm = "brute").fit(X)

# Bloc de mise en forme pour utilisateur
with st.form("form1"):
            films = st.selectbox("Films : ", liste_films_deroulante_films)
            submit1 = st.form_submit_button(label="Recherche")
if submit1:      
# Machine Learning Partie 2
# Création liste de film
        liste_du_film = films

# Obtenir tous les renseignements du film
        df_film_choisi = df2[(df2["primaryTitle"] == films) | (df2["originalTitle"] == films) | (df2["frenchTitle"] == films)]

# On ne selectionne que les colonnes contenant des booleens sur la ligne du film choisi
        film_choisi = df_film_choisi.iloc[:, 4:]

# Création de la matrice pour rechercher les index des plus proches voisins
        matrice_des_plus_proches_voisins = distanceKNN.kneighbors(film_choisi)

# Création de la liste des suggestions à partir de la matrice
        suggestion = df2.iloc[matrice_des_plus_proches_voisins[1][0][1:], 0].values
        st.subheader("Je te propose :")

# Création d'une variable pour récupérer le nom du film
        nom_du_filmFR = df2.iloc[matrice_des_plus_proches_voisins[1][0][1:], 3].values
        nom_du_filmEN = df2.iloc[matrice_des_plus_proches_voisins[1][0][1:], 1].values

# Création de colones
        col1 = st.columns(3)
     
# Boucle sur tconst et suggestion
        for film, nomFR, nomEN, colonnes in zip(suggestion, nom_du_filmFR, nom_du_filmEN, col1):
            with colonnes :
                url = url_api + str(film) + key_api
                url_imdb2 = url_imdb + str(film)
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    url_image = data['Poster']
                    st.image(url_image, width=200)
                except requests.exceptions.RequestException as e:
                    print("Une erreur est survenue lors de l'appel à l'API :", e)
                if type(nomFR) == str:
                    st.write(f" - [{nomFR}]({url_imdb2})")
                else:
                    st.write(f" - [{nomEN}]({url_imdb2}) ")

                
                
# Deuxième choix de filtre par acteur ou genre ou années
st.subheader("Ou alors choisis parmi :")

liste_films_deroulante_genres = [""] + list(df_genres2["genres"])
liste_deroulante_acteur = ["Tape ou recherche l'acteur(trice) de ton choix"] + list(df_films_note2["primaryName"])

with st.form("form2") :
            col1, col2, col3 = st.columns(3)
            with col1 :
                genres = st.multiselect(label = "Genres :", options = liste_films_deroulante_genres)
            with col2 :
                acteurs = st.selectbox(label = "Acteur(trice) :", options = liste_deroulante_acteur)
            with col3 :
                debut_annees, fin_annees = st.select_slider(label = "Sélectionne une fourchette d'années", options = df_annee["startYear"], value = (1913,2023))
            submit2 = st.form_submit_button(label = "Recherche")

if submit2:

    film_choisi1 = pd.merge(df_annee[df_annee['startYear'].between(debut_annees, fin_annees)], df2, how = 'left', left_on = 'tconst', right_on = 'tconst')
    st.subheader("Pour le(s) genre(s) choisis voici une recommandation :")

    if genres != []:
        film_genres = pd.DataFrame()
        for genre in genres:
            film_genres = pd.concat([film_genres, film_choisi1[film_choisi1[genre] == True]])
        film_choisi2 = film_genres.drop_duplicates()
        top3 = film_choisi2.sort_values(by = "averageRating", ascending = False).iloc[:3, :]
        top3_tconst = top3.iloc[:3]["tconst"]
        top3_titreFR = top3.iloc[:3]["frenchTitle"]
        top3_titreEN = top3.iloc[:3]["originalTitle"]

        colfilm2 = st.columns(3)   
        
        for colonne, tconst, titreFR, titreEN in zip(colfilm2, top3_tconst, top3_titreFR, top3_titreEN):
            with colonne :
                url2 = url_api + str(tconst) + key_api
                url_imdb2 = url_imdb + str(tconst)
                try:
                    response = requests.get(url2)
                    response.raise_for_status()
                    data2 = response.json()
                    url_image2 = data2['Poster']
                    st.image(url_image2, width=200)
                except requests.exceptions.RequestException as e:
                    print("Une erreur est survenue lors de l'appel à l'API :", e)
                if type(titreFR) == str:
                    st.write(f" - [{titreFR}]({url_imdb2}) ")
                else:
                    st.write(f" - [{titreEN}]({url_imdb2})")
     
    
    if acteurs != "Tape ou recherche l'acteur(trice) de ton choix":
        film_choisi3 = df2[df2[acteurs] == True]
        st.subheader("Pour l' acteur(trice) choisi voici une recommandation :")
    
        colfilm3 = st.columns(3)   

        top3 = film_choisi3.sort_values(by = "averageRating", ascending = False).iloc[:3, :]
        top3_tconst = top3.iloc[:3]["tconst"]
        top3_titreFR = top3.iloc[:3]["frenchTitle"]
        top3_titreEN = top3.iloc[:3]["originalTitle"]
        
        
        for colonne, tconst, titreFR, titreEN in zip(colfilm3, top3_tconst, top3_titreFR, top3_titreEN):
            
            with colonne :
                url2 = url_api + str(tconst) + key_api
                url_imdb2 = url_imdb + str(tconst)
                try:
                    response = requests.get(url2)
                    response.raise_for_status()
                    data2 = response.json()
                    url_image2 = data2['Poster']
                    st.image(url_image2, width=200)
                except requests.exceptions.RequestException as e:
                    print("Une erreur est survenue lors de l'appel à l'API :", e)
                if type(titreFR) == str:
                    st.write(f" - [{titreFR}]({url_imdb2})")
                else:
                    st.write(f" - [{titreEN}]({url_imdb2})")



# Subheader
    st.subheader("Bon visionnage ! ❤")

    