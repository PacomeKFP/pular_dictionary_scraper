#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import requests
import json
import time
from bs4 import BeautifulSoup


# Le Configurations de base du projet:
# la langue pour laquelle on souhaite reccuperer la bible ainsique les differents livres de la bible qui existe
# 
# _gen1_ represente le premier livre de la Genèse
# C'est le livre par defaut du site
# 

# Commençons par chercher tous les id de livres, pour cela on cherche juste les valuers des attributs _`data-vars-event-label`_ des elements selectionnés par _`ul.list.ma0.pa0.bg-white.pb5.min-vh-100 li`_ ceci sera fait grace à la console du navigateur puis on mettra le resultat dans un fichier json _utils/livres.json_
# 

# In[2]:


# Langue dans laquelle on va travailler
lang = 2826  # bible en Haussa avec caractères type arabique

VERSE_SELECTOR = ".yv-gray50.lh-copy.f3-m"

# fichier de sauvegardes des sessions
SESSIONS_PATH = os.path.join(os.getcwd(), 'sessions.json')


# dossier dans lequel on va mettre les dossiers chaque chapitre pour cette langue
def get_lang_folder_path(lang: int = lang) -> str:
    path = os.path.join(os.getcwd(), f"/data/{lang}")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# dossier dans lequel on va mettre les fichiers txt pour chaqe chap du livre livre
def get_book_folder_path_for_lang(book: str, lang: int = lang) -> str:
    path = os.path.join(os.getcwd(), f"data/{lang}/{book}").replace('\\', '/')

    if not os.path.exists(path):
        print(f'Path to saves folder created : {path} ')
        os.makedirs(path)
    return path


# chargeons les livres
with open('utils/livres.json', 'r') as books_file:
    books = json.load(books_file)

# 1er chapoitre du livre de la genese dans la langue en cours
gen1 = requests.get(f"https://www.bible.com/bible/{lang}/GEN.1.NFC")


def chapter_link(chapter: str, lang: int = lang) -> str:
    return f"https://www.bible.com/bible/{lang}/{chapter}"


def verse_link(chapter: str, verse: int, lang: int = lang) -> str:
    return f"https://www.bible.com/bible/{lang}/{chapter}.{verse}"


# La methode qui nous permettra d'effectuer nos requettes au serveur afin d'obtenir les differentes ressources dont on aura besoin
# 

# In[14]:


def fetch(url: str):
    fetched, try_count = False, 0
    def wait_time(count=try_count) -> int: return 5 if count < 10 else 10
    while not fetched:
        try:
            res = requests.get(url, timeout=15)
        except Exception as e:
            print('Request Failed please, check your internet connexion')
            try_count += 1
            if try_count > 5:
                print(f'Automatic retry in {wait_time()} secs .....')
                time.sleep(wait_time())
        else:
            fetched = True
            return res


# Pour trouver les differents chapitres d'un livres, nous exploiterons une API presente sur le site, elle nous permettra à partir du numero de la langue et de l'id du livre, d'obtenir les id de tous les chapitres contenus dans ce livre
# 

# In[ ]:


# les urls des json des chapitres pour la langue en cours
chapters_url = f"https://www.bible.com/json/bible/books/{lang}"
chapters: dict[list] = {}
print("Looking for chapters of each book of the bible")
not_founds = 0
for book in books:

    res = fetch(f"{chapters_url}/{book}/chapters")
    if res.status_code == 500:
        print(f"[{book}] Not Found ..")
        not_founds += 1
        continue
    chapters[book] = []
    data = json.loads(res.content)
    for item in data['items']:
        chapters[book].append(item['usfm'])

    print(f"[{book}] Completed ..")

print(
    f"\n\n\n[{lang}] Chapter titles fetched with success, {not_founds} books not found")
chapters


# Sauvegarder les de chapitres par langue dans chaque langue aura un fichier json dans lequel on mettre un dicco.
# Le dossier `./utils/chapitres_id/` contiendra des fichiers json pour chaque langue, chaque fichier contiendra tous les id de chapitres rangés par livre
# 

# In[4]:


chapters_id_file = os.path.join(
    os.getcwd(), f'utils/chapitres_id').replace('\\', '/')
if not os.path.exists(chapters_id_file):
    os.makedirs(chapters_id_file)
with open(f'{chapters_id_file}/{lang}.json', 'w', encoding='utf-8') as lang_chaps_file:
    json.dump(chapters, lang_chaps_file, indent=4)


# Fonction qui nous permettra de mettre à jour un fichier json, qu'il soit de type `dictionnaire` ou `liste`, on utilisera cela pour les sauvegardes de sessions
# 

# In[55]:


def update_json_file(data,  file_path: str, type: type = list, lang: int = lang):
    path = os.path.join(os.getcwd(), file_path)
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write('[]') if type == list else file.write('{}')
    with open(path, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        if type == list:  # si nous sommes dans un liste
            file_data.append('[]')
        else:  # si c'est un dictionnaire plutot
            file_data[f'{lang}'] = data
        file.seek(0)
        json.dump(file_data, file, indent=4)


# Implementons les fonctions de sauvegarde et de reprise de sessions afin de pourvoir reprendre un scraping qui s'arrete de facon impromptue. Ces sauvegardes de sessions se feront en separant les langues.
# 

# In[58]:


def save_current_session(book: str, chapter: str, completed_books: list[str], lang: int = lang):

    session = {
        "last_book": book,
        "last_chapter": chapter,
        "completed_books": completed_books
    }
    update_json_file(session, SESSIONS_PATH, dict)


def load_last_session(lang: int = lang):
    default_session = ['', '', []]
    if not os.path.exists(SESSIONS_PATH):
        with open(SESSIONS_PATH, 'w', encoding='utf-8') as sessions_file:
            json.dump({lang: default_session}, sessions_file, indent=4)
        return ['', '', []]

    with open(SESSIONS_PATH, 'r', encoding='utf-8') as sessions_file:
        sessions = json.load(sessions_file)
        try:
            return sessions[f'{lang}']
        except KeyError:
            return default_session


def json_print(message, json_doc):
    print(message)
    print(json.dumps(json_doc, indent=4, separators=(',', ': ')))


# In[61]:


print("Loading last scraping session ...")
last_session = load_last_session()
json_print('The last session was:', last_session)

completed_books = last_session['completed_books']
last_chapter = last_session['last_chapter']
last_book = last_session['last_book']

for book_name in chapters:
    if book_name in completed_books:
        continue
    book = chapters[book_name]
    print(f'[{book_name}] Proceeding book ...')

    for chapter in book:

        if book_name == last_book and int(chapter.split('.')[1]) <= int(last_chapter.split('.')[1]):
            continue

        print(f'[{chapter}] Proceeding chapter...')
        # selectionner un chapitre ainsi que sa page/url
        chapter_res = fetch(chapter_link(chapter))
        # les versets du chapitre
        chapter_verses: list[str] = []

        verse_index = 1
        # commencer à cchercher les versets duc chapitre du livre dans lequel on est
        while True:
            verse_res = fetch(verse_link(chapter, verse_index))
            # si le verset n'existe pas on sera redirigé vers la page du chapitre
            soup = BeautifulSoup(verse_res.content, 'html.parser')
            verses = soup.select(VERSE_SELECTOR)
            if verse_res.url == chapter_res.url or verse_res.url == gen1.url or len(verses) == 0:
                break

            chapter_verses.append(verses[0].text.replace('\n', ' '))
            print(f"[{chapter}][{verse_index}] Verse fetched with success")
            verse_index += 1

        folder = get_book_folder_path_for_lang(book_name)

        with open(f'{folder}/{chapter}.txt', mode='w', encoding='utf-8') as verse_output_file:
            for verse in chapter_verses:
                verse.replace('\n', ' ')
                verse_output_file.write(verse.strip() + '\n')

        save_current_session(book_name, chapter, completed_books)
        print(f'[{chapter}] done')

    completed_books.append(book_name)
    save_current_session(book_name, chapter, completed_books)
    print(f'[{book_name}] done')

