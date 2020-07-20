import requests
from dateutil.parser import parse
from constants import Category, Game, Section, Sort
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017')
db_collection = mongo_client.mods.mods

MODS_PATH = './mods/'
PAGE_SIZE = 200

latestMod = db_collection.find().sort("dateModified", -1).limit(1)
prevLatestDate = parse(latestMod[0]["dateModified"])

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
    # should limit to only mods that have a newer dateModified
    for mod in mods:
        dateModified = parse(mod['dateModified'])

        if parse(mod['dateModified']) <= prevLatestDate:
            done = True
            break
        else:
            db_collection.replace_one({'id': mod['id']}, mod, upsert=True)
            updated_count = updated_count + 1

    if len(mods) < 25 or done:
        break

print("Updates found:", updated_count)
