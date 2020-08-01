from flask import Flask, abort, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps

# mongo_client = MongoClient('mongodb://localhost:27017')

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/mods"
mongo = PyMongo(app)


@app.route('/mods', methods=["GET"])
def mods():
    documents = mongo.db.mods.find({}).sort("dateModified", -1).limit(25)
    return Response(dumps(documents), mimetype="application/json")


@app.route('/mods/<int:mod_id>', methods=["GET"])
def get_mod(mod_id):
    mod = mongo.db.mods.find_one({"id": mod_id})
    if mod is None:
        abort(404)
    return dumps(mod)


if __name__ is "__main__":
    app.run()
