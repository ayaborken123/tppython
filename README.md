Projet Movie API avec FastAPI & Groq API
Description
Ce projet est une API REST développée avec FastAPI qui permet de gérer une base de données de films et acteurs. Il intègre également une fonctionnalité de génération de résumés de films via l’API Groq (modèle de langage).

L’API permet :

Ajouter des films avec leurs acteurs.

Récupérer un film aléatoire.

Interroger le modèle Groq pour des réponses basées sur un prompt.

Générer un résumé automatique pour un film donné.

Technologies utilisées
Backend : Python 3.10+, FastAPI, SQLAlchemy, PostgresSgl

API externe : Groq API pour la génération de texte

Environnement : gestion avec .env pour la clé API Groq

Frontend : Stramlit

Prérequis
Python 3.10 ou plus

pip installé

Base de données PostgresSgl (intégrée) ou autre base SQL compatible SQLAlchemy

Clé API Groq (à obtenir sur https://console.groq.com/)

Installation & configuration
Cloner le projet



git clone https://github.com/ton-utilisateur/ton-projet.git
cd ton-projet
Créer un environnement virtuel et l’activer


pip install -r requirements.txt
Configurer la clé API Groq

Créer un fichier .env à la racine du projet avec le contenu suivant :


GROQ_API_KEY=ta_clef_api_ici
Lancer l’application

uvicorn main_fastapi:app --reload
L’API sera disponible sur : http://127.0.0.1:8000

Description des endpoints backend
Endpoint	Méthode	Description	Paramètres	Réponse
/movies/	POST	Crée un nouveau film avec ses acteurs	Body JSON : titre, année, etc.	Film créé (détail complet)
/movies/random/	GET	Récupère un film aléatoire avec ses acteurs	Aucun	Film aléatoire
/ask-groq	GET	Interroge le modèle Groq avec un prompt	Query param prompt	Résultat brut de l’API Groq
/generate_summary/	POST	Génère un résumé automatique pour un film donné	Body JSON : movie_id	Résumé généré