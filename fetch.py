import requests
import json
from urllib.parse import urlencode

LATEST_DATE_FILENAME = 'latestAddonDate.txt'

# TODO(dmauldin): read in latest addon fetch date
# latestDate = open(LATEST_DATE_FILENAME, 'r').read()
# print(latestDate)
quit()

ADDON_PATH = './addons/'

CATEGORY = {
    'All': 0
}

GAME = {
    'Minecraft': 432
}

SECTION = {
    'Mods': 6
}

SORT = {
    'LastUpdated': 2
}

params = {
    'categoryId': CATEGORY['All'],
    'gameId': GAME['Minecraft'],
    'gameVersion': '1.12.2',
    'index': 0,
    'pageSize': 25,
    'searchFilter': '',
    'sectionId': SECTION['Mods'],
    'sort': SORT['LastUpdated']
}

search_url = "https://addons-ecs.forgesvc.net/api/v2/addon/search"
headers = {'User-Agent': 'Mozilla/5.0'}

index = 0
while index < 400:
    params['index'] = index
    print(index)
    index += 1
    response = requests.get(search_url, params, headers=headers)
    for addon in response.json():
        filename = ADDON_PATH + addon['slug'] + ".json"
        open(filename, 'w').write(json.dumps(addon))
