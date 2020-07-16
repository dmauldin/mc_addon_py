import json
import requests
from dateutil.parser import parse
from datetime import datetime, timezone
from constants import Category, Game, Section, Sort
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017')
db_collection = mongo_client.mods.mods

LATEST_DATE_FILENAME = 'latestModDate.txt'
MODS_PATH = './mods/'
PAGE_SIZE = 200
nextLatestDate = None

try:
    file = open(LATEST_DATE_FILENAME, 'r')
    prevLatestDate = parse(file.read())
    file.close()
    # prevLatestDate = datetime(1, 1, 1, tzinfo=timezone.utc)
except FileNotFoundError:
    prevLatestDate = datetime(1, 1, 1, tzinfo=timezone.utc)

params = {
    'categoryId': Category.All,
    'gameId': Game.Minecraft,
    'gameVersion': '',
    'index': 0,
    'pageSize': PAGE_SIZE,
    'searchFilter': '',
    'sectionId': Section.Mods,
    'sort': Sort.LastUpdated
}

# "https://addons-ecs.forgesvc.net/api/v2/addon/search?categoryId=0&gameId=432&index=0&pageSize=25&searchFilter=&sectionId=6&sort=2"
search_url = "https://addons-ecs.forgesvc.net/api/v2/addon/search"
headers = {'User-Agent': 'Mozilla/5.0'}

updated_count = 0
done = False
# The CurseForge API has an 'index' limit of 9999
for index in range(0, 9999, PAGE_SIZE):
    params['index'] = index
    print('index: ', index)
    mods = requests.get(search_url, params, headers=headers).json()

    # TODO(dmauldin): update the replace_one call to do all 25 mods at a time
    for mod in mods:
        dateModified = parse(mod['dateModified'])

        if nextLatestDate is None:
            nextLatestDate = dateModified

        if dateModified <= prevLatestDate:
            done = True
            break
        else:
            db_collection.replace_one({'id': mod['id']}, mod, upsert=True)
            updated_count = updated_count + 1

            # TODO(dmauldin): eventually remove this when the mongo code is stable
            filename = MODS_PATH + mod['slug'] + ".json"
            with open(filename, 'w') as mod_file:
                mod_file.write(json.dumps(mod))

            if dateModified > nextLatestDate:
                nextLatestDate = dateModified

    if len(mods) < 25 or done:
        break

if nextLatestDate is not None:
    file = open(LATEST_DATE_FILENAME, 'w')
    file.write(nextLatestDate.isoformat())

print("Updates found:", updated_count)
