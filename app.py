from bson.json_util import dumps
from flask import Flask, Response, abort
from flask_pymongo import PyMongo
import json

# mongo_client = MongoClient('mongodb://localhost:27017')

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/mods"
mongo = PyMongo(app)


@app.route('/mods', methods=["GET"])
def mods():
    documents = mongo.db.mods.find({}).sort("dateModified", -1).limit(25)
    mods = json.loads(dumps(documents))
    print(mods)
    slugs = []
    for mod in mods:
        slugs.append(
            {'slug': mod['slug'], 'name': mod['name'], 'summary': mod['summary'], 'latest': mod['latestFiles'][0]['displayName']})
    return Response(dumps(slugs), mimetype="application/json")


@app.route('/mods/id/<int:mod_id>', methods=["GET"])
def get_mod_by_id(mod_id):
    mod = mongo.db.mods.find_one({"id": mod_id})
    if mod is None:
        abort(404)
    return dumps(mod)


@app.route('/mods/slug/<string:slug>', methods=["GET"])
def get_mod_by_slug(slug):
    mod = mongo.db.mods.find_one({"slug": slug})
    if mod is None:
        abort(404)
    return dumps(mod)


if __name__ is "__main__":
    app.run()
