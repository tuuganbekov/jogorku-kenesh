import requests
from bs4 import BeautifulSoup
import json
from db_connect import *

URL = 'http://kenesh.kg/ru/deputy/list/35'
LINK = 'http://kenesh.kg/'
HEADERS = {
    "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    "accept": '*/*',
}


def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    people = soup.find_all('div', class_='dep-item')
    # print(people)
    deputies = []

    for person in people:
        deputies.append({
            "name": person.find('a', class_='name').get_text(),
            "info": person.find('div', class_='info').get_text(),
            "image_link": LINK + person.find('img')['src'],
            "phone": person.find('span').get_text() if len(person.find('div', class_='bottom-info').get_text()) >= 2 else '',
        })
    return deputies


def return_json(deputies):
    with open('deputies.json', 'w') as file:
        json.dump(deputies, file, ensure_ascii=False, indent=3)


def write_to_db(deputies):
    for person in deputies:
        person = Person(name=person['name'], info=person['info'],
                        phone=person['phone'], image_link=person['image_link'],
                        )

        person.save()


def parse():
    html = get_html(URL)
    get_content(html)
    deputies = get_content(html)
    return_json(deputies)
    write_to_db(deputies)


parse()
