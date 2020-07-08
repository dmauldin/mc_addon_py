import glob
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.mods

files = glob.glob('./mods/*.json')

for file in files:
    mod_file = open(file, 'r')
    mod_json = json.loads(mod_file.read())
    mod_file.close()
    db.mods.replace_one({'id': mod_json['id']}, mod_json, upsert=True)

client.close()
