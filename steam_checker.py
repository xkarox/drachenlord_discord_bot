import urllib.request

import requests
import json

payload = { 'key': '671AB2FA9F97726BC387EE289AFCF351', 'steamid': '76561198060451501', 'include_appinfo': 'true'}

r = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v1', params=payload)
print(r.status_code)
print(r.url)
with open('drache_lib.json', "w") as f:
    json.dump(r.json(),f)

#pic = requests.get('http://media.steampowered.com/steamcommunity/public/images/apps/17390/75a96828a453586042ec4231e617070bc2f35625.jpg')
urllib.request.urlretrieve("http://media.steampowered.com/steamcommunity/public/images/apps/17390/00e6b5f1f7173e5a2db9978de34df03abb886430.jpg", "local-filename.jpg")

