# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 17:56:22 2019

@author: Diego Wanderley
@python: 3.6
@description: Set database reading XML and images
"""

import os
import arrow
import json
import pymongo
import xmltodict
import numpy as np
from PIL import Image
from classes import *


# Get scret data to access database
KEYS_FILE = '../python/keys.json'
DB_KEYS = json.load(open(KEYS_FILE))
# DB user (admin)
DB_USER = DB_KEYS["user"]
# Connection string
DB_URI = DB_KEYS["uri_header"] + "://" + DB_USER["username"] + ":" + DB_USER["password"] + "@" + DB_KEYS["host"]
# Read DB
client = pymongo.MongoClient(DB_URI)
db = client.get_database('screendr_db')

data_path = "//192.168.106.134/Diego Wanderley/Ultrasonix/organized/Data"

# Color values
c_point = [0,252,54]
c_measure = [0,255,255]
c_auto = [150,150,150]
c_yinfo = [210,210,0]

# Get file list
filelist = [f[:-4] for f in os.listdir(data_path) if f.endswith('.png')]

# Read data
for fname in filelist:
    # Check if image_id is new
    if (db.images.find({'image_id': { "$in": fname}}).count() == 0):
    {
        # Create object image data
        image_data = ImageData(uid=fname, folder="./gallery/")
        # Patient ID
        pid = fname.split('_')[1]
        image_data.patient_id = pid
        # Set path
        path_png = os.path.join(data_path, fname + '.png')
        # Read Image
        img = Image.open(path_png).convert("RGB")
        img_np = np.array(img)
        h, w, d = img_np.shape
        image_data.height = h
        image_data.width = w
        # Set FOV
        fov = img_np[100:700, 80:680, :]

        # Get indexes
        i_point = np.where(np.all(fov == c_point, axis=-1))
        i_measure = np.where(np.all(fov == c_measure, axis=-1))
        i_auto = np.where(np.all(fov == c_auto, axis=-1))
        i_yinfo = np.where(np.all(fov == c_yinfo, axis=-1))

        # Check 
        marks = ""
        if (len(i_point[0]) > 0):
            # has point
            marks = "point"
            if (len(i_measure[0]) > 0):
                # has measurements
                marks = "measurements"
                if ((len(i_auto[0]) > 0) and (len(i_yinfo[0]) > 0)):
                    # has autofolicle
                    marks = "auto_follicle"
        image_data.marks = marks

        ### XML ###
        path_xml = os.path.join(data_path, fname + '.xml') 
        xml_doc = None
        with open(path_xml) as fd:
            xml_doc = xmltodict.parse(fd.read())
        # Full object    
        image_data.acquisition_data = xml_doc['object']
        # Date acquisition
        xml_date = xml_doc['object']['time']
        date_acq = arrow.Arrow(int(xml_date['@year']),
                            int(xml_date['@month']),
                            int(xml_date['@day']),
                            hour=int(xml_date['@hour']),
                            minute=int(xml_date['@minute']),
                            second=int(xml_date['@second']))
        date_acq_zulu = "{}Z".format(date_acq.format('YYYY-MM-DDTHH:mm:ss.SSS'))    
        image_data.date_acquisition = date_acq_zulu
        # Upload date
        date_upload_zulu = "{}Z".format(arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss.SSS'))
        image_data.date_upload = date_upload_zulu

        # Update dataset
        db.images.insert_one(im_data)
    }

    print('')