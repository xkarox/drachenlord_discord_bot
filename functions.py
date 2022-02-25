# functions.py --
import os
import configparser
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from pandas import DataFrame
from googleapiclient.discovery import build


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

def get_steam_status(*args):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if len(args) == 0:
        STEAM_URL = config.get('Links', 'steam_url_drachenlord')
    else:
        STEAM_URL = args[0]
        print(STEAM_URL)
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

def get_youtube_livestream():
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    config = configparser.ConfigParser()
    config.read('config.ini')
    livestream_channel_id = config.get('Other', 'livestream_channel_id')

    with build('youtube', 'v3', developerKey = api_key) as youtube:
        request = youtube.search().list(part = 'snippet',
                channelId = livestream_channel_id,
                type = 'video',
                eventType = 'live',
                maxResults = 1
                )

        response = request.execute()
        return response
        #print(response['items'][0]['snippet']['title'])
if __name__ == '__main__':
    get_youtube_livestream()
