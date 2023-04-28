import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    layout="wide",
    page_icon="🎞️")

#title
st.title("Bienvenue dans notre humble application de remmandation de film")

# Header
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")
 
# Subheader
#st.subheader("This is a subheader")

# Text
#st.text("Hello GeeksForGeeks!!!")

# Markdown
#st.markdown("### This is a markdown")

# success
#st.success("Success")
 
# success
#st.info("Information")
 
# success
#st.warning("Warning")
 
# success
#st.error("Error")

# Write text
#st.write("Text with write")
 
# Writing python inbuilt function range()
#st.write(range(10))

# Display Images
# import Image from pillow to open images
#from PIL import Image
#img = Image.open("streamlit.png")
 
# display image using streamlit
# width is used to set the width of an image
#st.image(img, width=200)

# checkbox
# check if the checkbox is checked
# title of the checkbox is 'Show/Hide'
#if st.checkbox("Show/Hide"):
   
  # display the text if the checkbox returns True value
  #st.text("Showing the widget")

# radio button
# first argument is the title of the radio button
# second argument is the options for the ratio button
#status = st.radio("Select Gender: ", ('Male', 'Female'))
 
# conditional statement to print
# Male if male is selected else print female
# show the result using the success function
#if (status == 'Male'):
    #st.success("Male")
#else:
    #st.success("Female")
    
# multi select box
# first argument takes the box title
# second argument takes the options to show
   
with st.form("form 4"):
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            films = st.selectbox("Films : ", ['Dis moi quel film tu aimes', 'Film1', 'film2', 'film3'])
            st.write("Tu as choisis : ", films, ". Bon choix ;)")
        with col2 : 
            genres = st.multiselect("Genres : ", ["Drama", "Comedy,Drama", "Drama,Romance", "Documentary", "Comedy"])
            st.write("Tu as choisis", len(genres), 'genre(s)')
        with col3 : 
            acteurs = st.multiselect("Acteurs : ", ["Leo", "Alain", "Clint", "Marylin"])
            st.write("Tu as choisis", len(acteurs), 'acteur(trice)')
        with col4 : 
            année = st.slider("Année", 1913, 2023)
            st.text('Choisie : {}'.format(année))
        submit : st.form_submit_button("Soumettre")

if submit :
    st.writer("Tu recherches un film qui ressemble à : ",{films},"alors je te propose ces 3 films")


# Subheader
st.subheader("Bon visionnage !")
