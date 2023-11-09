import os
import requests
from bs4 import BeautifulSoup


SECRET_URL = os.environ.get("SECRET_URL")


with open("README.md", "r", encoding='utf-8') as f:
    read = f.read()

soup = BeautifulSoup(read, 'html.parser')

quote = soup.find(id="quote").text
movie = soup.find(id="movie").text


requests.post(SECRET_URL,
              headers={"Title": "Citation de film du jour !",
                       "Tags": "clapper"},
              data=f"{quote}{movie}".encode(encoding='utf-8')
              )
