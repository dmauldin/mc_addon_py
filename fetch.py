import json
import requests
from dateutil.parser import parse
from datetime import datetime, timezone
from constants import Category, Game, Section, Sort
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017')
db_collection = mongo_client.mods.mods

LATEST_DATE_FILENAME = 'latestModDate.txt'

try:
    file = open(LATEST_DATE_FILENAME, 'r')
    prevLatestDate = parse(file.read())
    file.close()
except FileNotFoundError:
    prevLatestDate = datetime(1, 1, 1, tzinfo=timezone.utc)

nextLatestDate = None

MOD_PATH: str = './mods/'

params = {
    'categoryId': Category.All,
    'gameId': Game.Minecraft,
    'gameVersion': '1.12.2',
    'index': 0,
    'pageSize': 25,
    'searchFilter': '',
    'sectionId': Section.Mods,
    'sort': Sort.LastUpdated
}

search_url = "https://addons-ecs.forgesvc.net/api/v2/addon/search"
headers = {'User-Agent': 'Mozilla/5.0'}

index = 0
updated_count = 0

# The API has a limit of index < 10000, which is 400 * 25
while index < 10_000:
    params['index'] = index
    print('index: ', index)
    index += 25
    response = requests.get(search_url, params, headers=headers)
    mods = response.json()

    # TODO(dmauldin): update the replace_one call to do all 25 mods at a time
    for mod in mods:
        dateModified = parse(mod['dateModified'])

        if nextLatestDate is None:
            nextLatestDate = dateModified

        if dateModified > prevLatestDate:
            db_collection.replace_one({'id': mod['id']}, mod, upsert=True)
            filename = MOD_PATH + mod['slug'] + ".json"
            # TODO(dmauldin): eventually remove this when the mongo code is stable
            with open(filename, 'w') as mod_file:
                mod_file.write(json.dumps(mod))
            updated_count = updated_count + 1

            if dateModified > nextLatestDate:
                nextLatestDate = dateModified

    if len(mods) < 25:
        break

if nextLatestDate is not None:
    file = open(LATEST_DATE_FILENAME, 'w')
    file.write(nextLatestDate.isoformat())

print("Updates found:", updated_count)
