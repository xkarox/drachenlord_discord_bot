import os

from functions import get_current_steam_game, get_steam_status

import requests
import json
from PIL import Image
import matplotlib.pyplot as plt

lib = 'drache_lib.json'

__all__ = ['get_number_of_games_owned', 'get_current_game_name_and_image_url']


def __get_lib():
    if os.path.exists(lib):
        print("Lib loaded")
    else:
        __save_games_to_json()


def __get_owned_games(steamid, get_drache):
    key = os.getenv('STEAM_API_KEY')

    if get_drache:
        steamid = os.getenv('STEAM_ID_DRACHE')

    payload = {'key': key, 'steamid': steamid, 'include_appinfo': 'true'}
    r = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v1', params=payload)
    print(r.status_code)
    print(r.url)
    return r


def __save_games_to_json():
    request = __get_owned_games('0', True)
    with open(lib, "w") as f:
        json.dump(request.json(), f)


def __get_appid_and_img_url(name):
    with open(lib) as jsonFile:
        data = json.load(jsonFile)
        json_data = data["response"]["games"]
        for items in json_data:
            if name == items['name']:
                appid = items['appid']
                img_url = items['img_logo_url']
                return appid, img_url


def __get_game_image_url(name):
    appid, image_url = __get_appid_and_img_url(name)
    return f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{image_url}.jpg"


def get_current_game_name_and_image_url(*args):
    # Returns the name and Image of Drachenlords current steam game
    __get_lib()
    if len(args) == 0:
        steam_status = get_steam_status()
    else:
        steam_status = get_steam_status(args[0])
    if steam_status == "Currently In-Game":
        game_name = get_current_steam_game()
        print("Drache ist Ingame")
        game_img = __get_game_image_url(game_name)
        return game_name, game_img
    else:
        print("Drache ist nicht Ingame")


def get_number_of_games_owned():
    # Returns the number of Games Drache currently owns
    with open(lib) as jsonFile:
        data = json.load(jsonFile)
        return data["response"]['game_count']


# ------------------- Example -------------------------

def example_cookie():
    print("Example request")
    # request = get_owned_games('0', True)
    # save_request_to_json(request)
    # dataFrame = save_request_to_dataframe(request)
    name, img = get_current_game_name_and_image_url()
    print(name)
    print(get_number_of_games_owned())
    plt.imshow(img)
    plt.show()


def main():
    example_cookie()


if __name__ == '__main__':
    main()
