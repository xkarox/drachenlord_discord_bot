# functions.py --

import os
import configparser
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from pandas import DataFrame

def update_steam_games():
    #updatet die steam spiele liste
    #http://api.steampowered.com/ISteamApps/GetAppList/v0002/

def get_app_id():
    #pandas dataframe
    # oder pack die scheisse in eine datenbank
    #oder pandas dataframe -> array
    #steam api -> steam spiele eines users mit zuätzlichen infos

def get_stats():
    r = requests.get('https://drachenchronik.com/')
    soup = BeautifulSoup(r.content, 'html.parser')
    dataThisMonth = {}
    dataToday = {}

    month_HTML = soup.select('.box.color.half')[1].text.strip()
    month_Data = re.findall('(.*)', month_HTML)
    for i in month_Data:
        if i == '': month_Data.remove(i)
    month_Date = month_Data[0]
    month_Video = month_Data[1]
    month_Streams = month_Data[2]
    month_Money = month_Data[3]
    #print(f'Date: {month_Date}\nVideos: {month_Video}\nStreams: {month_Streams}\nMoney: {month_Money}')

    day_HTML = soup.select('.box.color.half')[0].text.strip()
    day_Data = re.findall('(.*)', day_HTML)
    for i in day_Data:
        if i == '': day_Data.remove(i)
    day_Date = day_Data[0]
    day_Video = day_Data[1]
    day_Streams = day_Data[2]
    day_Money = day_Data[3]


    return month_Date, month_Video, month_Streams, month_Money, day_Date, day_Video, day_Streams, day_Money

def get_images():
    load_dotenv()
    STEAM_URL = os.getenv('DISCORD_STEAM_URL')
    r = requests.get('https://drachenchronik.com/image/search?t=2')
    soup = BeautifulSoup(r.content, 'html.parser')

    x = soup.select('img')

    print(x)

def get_steam_status():
    config = configparser.ConfigParser()
    config.read('config.ini')
    STEAM_URL = config.get('Links', 'steam_url_drachenlord')
    r = requests.get(STEAM_URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    profile_in_game_header = soup.select_one('.profile_in_game_header').text.strip()

    return profile_in_game_header

def get_current_steam_game():
    config = configparser.ConfigParser()
    config.read('config.ini')
    STEAM_URL = config.get('Links', 'steam_url_drachenlord')
    r = requests.get(STEAM_URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    profile_in_game_name = soup.select_one('.profile_in_game_name').text.strip()

    return profile_in_game_name


if __name__ == '__main__':
    get_steam_status()
