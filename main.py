from bs4 import BeautifulSoup
import html
import json
import random


path_json = "data_quote.json"
path_history = "data_history.json"
path_readme = "README.md"
base_history = {"history_movie_choices": [],
                "history_quote_choices": []
                }


# load Database
with open(path_json, "r", encoding="utf-8") as f:
    db = json.load(f)

# load historique
with open(path_history, "r", encoding="utf-8") as f:
    history = json.load(f)


# On tire au sort parmi les films dans un premier temps
ids_movie = list(set(db["ids"]))
random_movie_choice = random.randint(0, len(ids_movie))
id_movie = ids_movie[random_movie_choice]
index_id = [i for i, valeur in enumerate(db["ids"]) if valeur == id_movie]

# Puis, on tire au sort la citation du film
random_quote_choice = random.randint(index_id[0], index_id[-1])

# Resultat
random_quote = db["quotes"][random_quote_choice]
random_character = db["character"][random_quote_choice]


if "\n" in random_quote:
    random_quote = random_quote.replace("\n", "<br>")


# verifie que le json a le meme modèle que le script
if base_history.keys() != history.keys():
    history = base_history
history["history_movie_choices"].append(id_movie)
history["history_quote_choices"].append(random_quote_choice)


# ajout du random choice actuel
with open(path_history, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=4)

# load le readme
with open(path_readme, "r") as f:
    read = f.read()


soup = BeautifulSoup(read, 'html.parser')

# Pour le bot
chosen = history["history_movie_choices"].count(id_movie)
days = len(history["history_movie_choices"])
total_movies = len(ids_movie)
WolfyBOT = f"🤖 WolfyBOT 🤖 vous informe que ce film a été tiré <b>{chosen}</b> fois au sort parmis les <b>{total_movies}</b> films sur <b>{days}</b> jours consécutifs. 🎲🎲🎲"


tag_quote = soup.find(id="quote")
tag_movie = soup.find(id="movie")
tag_bot = soup.find(id="bot")

tag_quote.string = random_quote
tag_movie.string = random_character
tag_bot.string = WolfyBOT

# Déséchapper les entités HTML
read_update = html.unescape(soup.prettify())

# SAVE README
with open(path_readme, "w", encoding="utf-8") as f:
    f.write(read_update)
