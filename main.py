import json
import os
import random

path_json = "data_quote.json"
path_history = "data_history.json"
path_readme = "README.md"
base_history = {"history_choices": []}
tag_quote_start = "<!-- INSERT QUOTE START -->"
tag_quote_end = "<!-- INSERT QUOTE END -->"

# load Database
with open(path_json, "r", encoding="utf-8") as f:
    db = json.load(f)

# load historique
with open(path_history, "r", encoding="utf-8") as f:
    history = json.load(f)

random_choice = random.randint(0, len(db["quotes"]))

random_quote = db["quotes"][random_choice]
random_character = db["character"][random_choice]


if "\n" in random_quote:
    random_quote = random_quote.replace("\n", "\n\n")


# verifie que le json a le meme modèle que le script
if base_history.keys() != history.keys():
    history = base_history
history["history_choices"].append(random_choice)

total_history_quote = len(history["history_choices"])

# ajout du random choice actuel
with open(path_history, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=4)

# load le readme
with open(path_readme, "r") as f:
    read = f.read()

index_start = read.find(tag_quote_start)
index_end = read.find(tag_quote_end)

if index_start != -1 and index_end != -1:
    read_update = (f"{read[:index_start + len(tag_quote_start)]} \n\n\" {random_quote} \"\n\n_{random_character}_\n\n"
                   f"{read[index_end:]}")

    with open(path_readme, "w", encoding="utf-8") as f:
        f.write(read_update)
