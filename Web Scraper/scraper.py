import os
import re
import requests
from string import punctuation
from bs4 import BeautifulSoup

LINK = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'

pages, theme = int(input()), input()
for i in range(1, pages + 1):
    os.mkdir(f'./Page_{i}')
    articles = BeautifulSoup(requests.get(f'{LINK}&page={i}').content, 'html.parser').find_all('article')
    target_links = [a.find('a', {'data-track-action': 'view article'}).get('href') for a in articles if
                    a.find('span', {'class': 'c-meta__type'}).text == theme]
    for link in target_links:
        article_data = BeautifulSoup(requests.get(f'https://www.nature.com{link}').content, 'html.parser')
        name = re.sub(f'[{punctuation}]', '', article_data.find('title').text.strip()).replace(' ', '_')
        content = article_data.find('p', {'class': 'article__teaser'}).text
        with open(f'./Page_{i}/{name}.txt', 'wb') as outfile:
            outfile.write(content.encode())
