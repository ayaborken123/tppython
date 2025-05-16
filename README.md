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

🔹 Question 1 : Pourquoi est-il souvent nécessaire de valider (commit) l’enregistrement principal (Movies) avant de créer les enregistrements associés (Actors) qui dépendent de sa clé étrangère ?
Il est nécessaire de faire un commit() sur le film (Movies) avant de créer les acteurs (Actors), car :

L'identifiant (id) du film n'est généré qu'après avoir été enregistré dans la base de données.

Cet id est la clé étrangère (foreign key) nécessaire pour lier chaque acteur à son film via le champ movie_id.
📝 En résumé : On valide (commit) d’abord l’objet principal (Movies) pour s’assurer que son id est bien généré, afin de l’utiliser pour les objets enfants (Actors).

Question 2 : Quelle est la différence entre le chargement paresseux (lazy loading) et le chargement hâtif (eager loading) comme joinedload dans SQLAlchemy ?
Lazy loading (chargement paresseux) :
Les relations (ex. : liste des acteurs d’un film) ne sont chargées que lorsqu’on y accède. Cela déclenche une requête SQL supplémentaire.

movie = db.query(Movies).first()
actors = movie.actors  # une nouvelle requête est faite ici
Eager loading (chargement hâtif) avec joinedload :
SQLAlchemy charge immédiatement les données liées (comme les acteurs) dans une seule requête JOIN.

movie = db.query(Movies).options(joinedload(Movies.actors)).first()
📝 En résumé :

Lazy loading = + simple mais plus lent si on accède aux relations plusieurs fois (beaucoup de requêtes).

Eager loading = + performant pour charger tout d’un coup, idéal pour l'affichage de détails liés.

Question 3 : Comment formater la liste des acteurs récupérée depuis la base de données en une chaîne de texte simple pour l’inclure dans un prompt LLM ?
Tu peux convertir la liste des acteurs en une chaîne de noms séparés par des virgules :


actor_names = ", ".join(actor.actor_name for actor in movie.actors)
Par exemple, si tu as trois acteurs :


["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"]
Cela donne :

"Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page"
✅ Cette chaîne peut ensuite être insérée dans un prompt LLM comme :


f"Génère un résumé du film '{movie.title}' avec les acteurs {actor_names}."