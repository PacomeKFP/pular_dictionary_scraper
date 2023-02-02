from titanscraper import TitanScraper
import json
scraper = TitanScraper()
 
#loading rules and target
with open('data/targets.json', mode='r') as tg, open('data/rules.json', mode='r') as rl:
    targets = json.load(tg)
    RULES = json.load(rl)

# selectionner les onglets (alphabet)
alphabet = scraper.get_links_from_page(targets[0], '', 'lpTitleLetter')
with open('collected/alphabet', 'w') as f:
    json.dump(alphabet, f)


all_words_links = []
#ouvrir la page de chaque lettre et reccuperer les liens vers les mots
i = 1
for letter in alphabet:
    
    
    print(f'[{i}] Nouvelle lettre accomplie {letter}')
    i += 1


word_links_for_letter = scraper.get_links_from_page(targets[0], '', 'entry a')