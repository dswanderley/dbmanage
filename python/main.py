# -*- coding: utf-8 -*-
"""
Created on Wed Mar 03 10:39:30 2019

@author: Diego Wanderley
@python: 3.6
@description: Main script to manage a MongoDB database for DICOM images
"""


import json
import pymongo
from urllib.parse import quote_plus


# Get scret data to access database
KEYS_FILE = './keys.json'
DB_KEYS = json.load(open(KEYS_FILE))
# DB user (admin)
DB_USER = DB_KEYS["user"]
# Connection string
DB_URI = DB_KEYS["uri_header"] + "://%s:%s@%s" % (
    quote_plus(DB_USER["username"]), quote_plus(DB_USER["password"] ), DB_KEYS["host"])
DB_URI += "?retryWrites=true"

# Read DB
client = pymongo.MongoClient(DB_URI)
db = client.get_database('screendr_db')
print(db)

print('')

# Get Collection
coll_images = db.images
print(list(coll_images.find()))

