# -*- coding: utf-8 -*-
"""
Created on Tue May 07 16:43:40 2019

@author: Diego Wanderley
@python: 3.6
@description: Read DICOM files to save data on MongoDB Atlas.
"""


import os
import glob
import math
import datetime
import random
import pydicom
import cv2
import numpy as np


class ImageData:
    '''Define Image Data class'''
    def __init__(self, uid='', folder='./'):

        self.image_id = uid
        self.filename = uid + '.png'
        self.folder = folder
        self.path = folder + self.filename
        # Form information
        self.originalname = None
        self.date_acquisition = None
        self.date_upload = None
        self.observations = None    # Text field
        self.patient_id = None       # Text field
        self.eye = None             # Text field
        # File information
        self.height = None     # int
        self.width = None      # int
        self.file_type = None # string
        # Processing data
        self.processed = False
        self.date_processed = None
        self.quality = None # bool
        self.quality_pred = -1.0
        self.normality = None # bool
        self.normality_pred = -1.0
        self.grading = None # bool
        self.annotations = []

def filename_gen():
    ''' @description Generate data from '''

    date = datetime.datetime.now()
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text = ""

    msec = math.floor(date.microsecond / 10000)
    if msec > 61:
        msec = msec - 61
    hour = date.hour
    sec = date.second
    minutes = date.minute
    day = date.day
    year = date.year - 2000
    mon = date.month

    for _ in range(5):
        text += charset[random.randint(0, len(charset)-1)]
    text = charset[msec] + charset[hour] + charset[sec] + charset[minutes]
    for _ in range (6):
        text += charset[random.randint(0, len(charset)-1)]
    text += '_'
    text += charset[random.randint(0, len(charset))]
    text +=  charset[day] +  charset[year] +  charset[mon]
    for _ in range(6):
        text += charset[random.randint(0, len(charset)-1)]
    text += '_'
    for _ in range(10):
        text += charset[random.randint(0, len(charset)-1)]

    return text


# Root directory
I_DIR = '../images'
# Set of files
DICOM_LIST = (glob.glob(os.path.join(I_DIR + '/', '*.dcm')))
folder = '../upload/'

for dcm_str in DICOM_LIST:

    dcm = pydicom.dcmread(dcm_str)
    new_name = folder + filename_gen() + ".png"

    pixel_array_numpy = dcm.pixel_array
    pixel_array_numpy_2 = np.copy(pixel_array_numpy)
    pixel_array_numpy_2[...,0] = pixel_array_numpy[...,2]
    pixel_array_numpy_2[...,2] = pixel_array_numpy[...,0]

    im_id = dcm.SOPInstanceUID
    imdata = ImageData(uid=im_id, folder=folder)
    cv2.imwrite(new_name, pixel_array_numpy_2)

    imdata.eye = dcm.Laterality
    imdata.patient_id = dcm.PatientID
    imdata.width = dcm.Rows
    imdata.height = dcm.Columns
    print(imdata)
