# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 15:21:30 2019

@author: Diego Wanderley
@python: 3.6
@description: Exchange data on a document
"""


import json
import pymongo


# Get scret data to access database
KEYS_FILE = './keys_cber.json'
DB_KEYS = json.load(open(KEYS_FILE))
# DB user (admin)
DB_USER = DB_KEYS["user"]
# Connection string
# Connection string
DB_URI = DB_KEYS["uri_header_py3.6"] + "://" + DB_USER["username"] + ":" + DB_USER["password"] + "@" + DB_KEYS["host_py3.6"]

# Read DB
client = pymongo.MongoClient(DB_URI)
db = client.get_database('screendr_db')

# Get Collection
coll_images27 = db.images
print('Number of images (Collection):  {:d}'.format(coll_images27.count_documents({})))
coll_images36 = db.images36
print('Number of images (Collection):  {:d}'.format(coll_images36.count_documents({})))

# Convert colection to list
images27 = list(coll_images27.find({}))
images36 = list(coll_images36.find({}))

# Read collection 1
for im27 in images27:
    # Get data
    h = im27['width']
    w = im27['height']
    mongo_id = im27['_id']
    # Set data 
    im27['height'] = h
    im27['width'] = w
    # Update
    coll_images27.update_one({'_id':mongo_id}, {"$set": im27}, upsert=False)

# Read collection 2
for im36 in images27:
    # Get data
    h = im36['width']
    w = im36['height']
    mongo_id = im36['_id']
    # Set data 
    im36['height'] = h
    im36['width'] = w
    # Update
    coll_images36.update_one({'_id':mongo_id}, {"$set": im36}, upsert=False)
