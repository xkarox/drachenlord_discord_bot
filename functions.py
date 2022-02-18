# functions.py --

import requests
import bs4 import BeautifulSoup

def get_revenue():
    t = requests.get('https://drachenchronik.com/')
    soup = BeautifulSoup(r.content, 'html-parser')
    d = {}

    d['date'] = soup.select_one('.container .box .color .half')
