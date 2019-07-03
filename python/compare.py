# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:01:03 2019

@author: Diego Wanderley
@python: 3.6
@description: Compare to collections data
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

# Variables
images = ['image_id', 'qual_py27', 'qual_py36', 'norm_py27', 'norm_py36']
qual_mis = 0
norm_mis = 0
equals = 0
# Read collection 1
for im27 in images27:
    qual27 = im27['quality']
    norm27 = im27['normality']
    # Read collection 1
    for im36 in images36:
        qual36 = im36['quality']
        norm36 = im36['normality']

        # Compare if IDs are equal
        if (im36['image_id'] == im27['image_id']):
            equals  += 1

            # Create element / table row
            el = [
                im36['image_id'],
                qual27['q_pred'],
                qual36['q_pred'],
                norm27['dr_pred'],
                norm36['dr_pred']
            ]
            images.append(el)
            print(el)
            # Check quality
            if qual27['qual'] != qual36['qual']:
                qual_mis += 1
            # Check normaliy
            if norm27['dr'] != norm36['dr']:
                norm_mis += 1

            break


print('Images existing in both collections:  {:d}'.format(equals))
print('Quality   disagreements:  {:d}'.format(qual_mis))
print('Normality disagreements:  {:d}'.format(norm_mis))
