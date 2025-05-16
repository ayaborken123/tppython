import streamlit as st
import requests

# URL de ton backend FastAPI (adapter selon ton setup)
API_BASE_URL = "http://127.0.0.1:8000"

# --- Task 3.1: Streamlit App Structure ---
st.title("Movie Explorer")

# Initialisation de st.session_state pour garder les données persistantes
if "current_movie" not in st.session_state:
    st.session_state.current_movie = None
if "summary_text" not in st.session_state:
    st.session_state.summary_text = None

# --- Task 3.2: Implement "Explore Movies" UI (Data Display) ---

def show_random_movie():
    try:
        response = requests.get(f"{API_BASE_URL}/movies/random/")
        response.raise_for_status()
        movie_data = response.json()
        
        # Stockage dans session_state
        st.session_state.current_movie = movie_data
        st.session_state.summary_text = None  # Reset summary quand un nouveau film est chargé
    except requests.RequestException as e:
        st.error(f"Erreur lors de la récupération du film aléatoire : {e}")

# Bouton pour charger un film aléatoire
if st.button("Show Random Movie"):
    show_random_movie()

# Affichage des détails du film s'il y en a un en session_state
if st.session_state.current_movie:
    movie = st.session_state.current_movie
    st.header(f"{movie['title']} ({movie['year']})")
    st.write(f"**Director:** {movie['director']}")
    st.subheader("Actors:")
    for actor in movie.get("actors", []):
        st.write(f"- {actor['actor_name']}")

# --- Task 3.3: Implement "Explore Movies" UI (Summary Request) ---

def get_summary():
    if not st.session_state.current_movie:
        st.warning("Please load a movie first.")
        return

    payload = {"movie_id": st.session_state.current_movie["id"]}
    try:
        response = requests.post(f"{API_BASE_URL}/generate_summary/", json=payload)
        response.raise_for_status()
        summary_data = response.json()
        st.session_state.summary_text = summary_data.get("summary_text", "No summary received.")
    except requests.RequestException as e:
        st.error(f"Erreur lors de la génération du résumé : {e}")

# Bouton "Get Summary" activé uniquement si un film est chargé
if st.session_state.current_movie:
    if st.button("Get Summary"):
        get_summary()

# Affichage du résumé s'il existe
if st.session_state.summary_text:
    st.info(st.session_state.summary_text)
