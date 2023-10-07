import json
import os
import random

path_json = "data_quote.json"
path_history = "data_history.json"
path_readme = "README.md"
base_history = {"history_movie_choices": [],
                "history_quote_choices": []
                }
tag_quote_start = "<!-- INSERT QUOTE START -->"
tag_quote_end = "<!-- INSERT QUOTE END -->"

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
    random_quote = random_quote.replace("\n", "\n\n")


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


# Pour le bot plus tard
try:
    chosen = len(history["history_movie_choices"][id_movie])
except IndexError:
    chosen = 0
total_movies = len(ids_movie)
WolfyBOT = f"🤖 WolfyBOT 🤖 vous informe que ce film a été tiré **{chosen}** fois au sort parmis les **{total_movies}**. 🎲🎲🎲"


index_start = read.find(tag_quote_start)
index_end = read.find(tag_quote_end)

if index_start != -1 and index_end != -1:
    read_update = (f"{read[:index_start + len(tag_quote_start)]} \n\n\" {random_quote} \"\n\n_{random_character}_\n\n"
                   f"{read[index_end:]}")

    with open(path_readme, "w", encoding="utf-8") as f:
        f.write(read_update)
