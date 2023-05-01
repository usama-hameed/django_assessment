import pymongo
import os
myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
# db_name = os.environ.get("DB_Name")
# coll_name = os.environ.get("COLLECTION_NAME")

db = myclient["MoviesDB"]

collection = db["movies"]
