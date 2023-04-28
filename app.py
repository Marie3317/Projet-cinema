import streamlit as st
import pandas as pd

# Chargement en local en pikle
liste_films = pd.read_pickle("liste_films.pkl.gz")
df_genres2 = pd.read_pickle("df_genres2.pkl.gz")
df_films_note2 = pd.read_pickle("df_films_note2.pk.gz")

# Configuration de la page
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    layout="wide",
    page_icon="🎞️")

#title
st.title("Bienvenue dans notre humble application de remmandation de film")

# Header
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")
 

liste_films_déroulante_films = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])

liste_films_déroulante_genres = list(df_genres2["genres"])

liste_deroulante_acteur = list(df_films_note2["primaryName"])


   
with st.form("form 4"):
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            films = st.selectbox("Films : ", liste_films_déroulante)
            st.write("Tu as choisis : ", films, ". Bon choix ;)")
        with col2 : 
            genres = st.multiselect("Genres : ", liste_films_déroulante_genres)
            st.write("Tu as choisis", len(genres), 'genre(s)')
        with col3 : 
            acteurs = st.multiselect("Acteurs : ", liste_deroulante_acteur)
            st.write("Tu as choisis", len(acteurs), 'acteur(trice)')
        with col4 : 
            année = st.slider("Année", 1913, 2023)
            st.text('Année choisie : {}'.format(année))
        submit : st.form_submit_button("Soumettre")


# Subheader
st.subheader("Bon visionnage !")
