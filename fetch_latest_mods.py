import requests
from dateutil.parser import parse
from constants import Category, Game, Section, Sort
from pymongo import MongoClient, ReplaceOne

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
    operations = []

    # should limit to only mods that have a newer dateModified
    for mod in mods:
        # TODO(dmauldin): this needs to be updated for anything other than sort by latest
        if parse(mod['dateModified']) <= prevLatestDate:
            done = True
            break
        else:
            # This is ReplaceOne instead of UpdateOne because we're receiving
            # the entire mod object from the API and it may include changes to
            # property names
            operations.append(ReplaceOne({'id': mod['id']}, mod, upsert=True))

    result = db_collection.bulk_write(operations)
    updated_count = updated_count + len(operations)

    if len(mods) < PAGE_SIZE or done:
        break

print("Updates found:", updated_count)
