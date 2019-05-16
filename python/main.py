# -*- coding: utf-8 -*-
"""
Created on Tue May 07 10:39:30 2019

@author: Diego Wanderley
@python: 3.6
@description: Main script to manage a MongoDB database for DICOM images
"""


import json
import pymongo
from read_dicom import *
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

# Get Collection
images = db.images
print('Number of images (before insertion):  {:d}'.format(images.count_documents({})))

# Process data
data_list = read_dcm_save_png()
# Store content (documents)
if len(data_list) == 1:
    images.insert_one(data_list[0])
elif len(data_list) > 1:
    images.insert_many(data_list)
else:
    pass

# New insertions
print('Number of images (after insertion):  {:d}'.format(images.count_documents({})))
