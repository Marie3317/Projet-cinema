import streamlit as st
import pandas as pd

# Chargement en local en pikle
liste_films = pd.read_pickle("liste_films.pkl.gz")
df_genres2 = pd.read_pickle("df_genres2.pkl.gz")
df_films_note2 = pd.read_pickle("df_films_note2.pkl.gz")
df_annee = pd.read_pickle("df_annee.pkl.gz")


# Configuration de la page
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    layout="wide",
    page_icon="🎞️")

#title
st.title("Bienvenue dans notre humble application de remmandation de film")

# Header
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")
 

liste_films_deroulante_films = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])
liste_films_deroulante_genres = list(df_genres2["genres"])
liste_deroulante_acteur = list(df_films_note2["primaryName"])
liste_deroulante_annee = list(df_annee["startYear"])

# Subheader
st.subheader("Choisi obligatoirement ton film préféré")

films = st.selectbox("Films : ", liste_films_deroulante_films)
st.write("Tu as choisis : ", films, ". Bon choix ;)")

# Subheader
st.subheader("Tu peux également choisir parmi les listes de choix suivantes")


with st.form("form 4"):
        col1, col2, col3 = st.columns(3)
        with col1 : 
            genres = st.multiselect(label = "Genres : ", options = liste_films_deroulante_genres)
            st.write("Tu as choisis", len(genres), 'genre(s)')
        with col2 : 
            acteurs = st.multiselect(label = "Acteurs : ", options = liste_deroulante_acteur)
            st.write("Tu as choisis", len(acteurs), 'acteur(trice)')
        with col3 : 
            start_year, end_year = st.select_slider(label = "Sélectionne une plage d'année", options = df_annee["startYear"], value = (1913, 2023))
            st.write("Tu as choisis une plage d'année entre", start_year, 'et', end_year)
        submit = st.form_submit_button("Soumettre")

            
if submit:
        st.write("Tu as choisi : {}, qui a pour genre(s) {}, avec les acteurs(trices) {}, et dont les années sont comprises entre {} et {}.".format
                 (films, "/".join(genres), "/".join(acteurs), start_year, end_year))
    
    
    
# Subheader
st.subheader("Bon visionnage !")
