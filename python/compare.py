# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:1:03 2019

@author: Diego Wanderley
@python: 3.6
@description: Compare to collections data
"""


import json
import pymongo
from urllib.parse import quote_plus

# Get scret data to access database
KEYS_FILE = './keys_cber.json'
DB_KEYS = json.load(open(KEYS_FILE))
# DB user (admin)
DB_USER = DB_KEYS["user"]
# Connection string
DB_URI = DB_KEYS["uri_header_py3.6"] + "://%s:%s@%s" % (
    quote_plus(DB_USER["username"]), quote_plus(DB_USER["password"] ), DB_KEYS["host_py3.6"])
DB_URI += "?retryWrites=true"

# Read DB
client = pymongo.MongoClient(DB_URI)
db = client.get_database('screendr_db')

# Get Collection
images27 = db.images
print('Number of images (before insertion):  {:d}'.format(images27.count_documents({})))
images36 = db.images36
print('Number of images (before insertion):  {:d}'.format(images36.count_documents({})))