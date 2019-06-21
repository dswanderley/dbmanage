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
    def __init__(self, uid='', filename='', folder='./'):

        self.image_id = uid
        self.filename = filename
        self.folder = folder
        self.path = folder + self.filename
        # Form information
        self.original_name = None
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
    text += charset[random.randint(0, len(charset)-1)]
    text +=  charset[day] +  charset[year] +  charset[mon]
    for _ in range(6):
        text += charset[random.randint(0, len(charset)-1)]
    text += '_'
    for _ in range(10):
        text += charset[random.randint(0, len(charset)-1)]

    return text


def read_dcm_save_png(in_dir='../images/dicom', out_dir='../images/upload/'):
    '''
        Save images as .png and returns list of images.
    '''
    # Root directory
    I_DIR = i_dir
    # Set of files
    DICOM_LIST = (glob.glob(os.path.join(I_DIR + '/', '*.dcm')))
    folder = out_dir

    output_data = []

    # Read input folder
    for dcm_str in DICOM_LIST:
        # Read DICOM
        dcm = pydicom.dcmread(dcm_str)
        im_id = dcm.SOPInstanceUID

        # Get image (as numpy)
        pixel_array_numpy = dcm.pixel_array
        pixel_array_numpy = np.copy(dcm.pixel_array)
        pixel_array_numpy[...,0] = dcm.pixel_array[...,2]
        pixel_array_numpy[...,2] = dcm.pixel_array[...,0]

        # save Image
        new_name = filename_gen() + ".png"
        cv2.imwrite(folder + new_name, pixel_array_numpy)

        # Set data        
        imdata = ImageData(uid=im_id, filename=new_name, folder=folder)
        # Aqusition datetime
        date_time = datetime.datetime(int(dcm.ContentDate[0:4]),
                                    int(dcm.ContentDate[4:6]),
                                    int(dcm.ContentDate[6:8]), 
                                    int(dcm.ContentTime[0:2]),
                                    int(dcm.ContentTime[2:4]),
                                    int(dcm.ContentTime[4:6]))
        imdata.date_acquisition = str(date_time)
        # Uplaod datetime
        imdata.date_upload = str(datetime.datetime.now())        
        # original name
        imdata.original_name = im_id + '.dcm'
        # laterality
        imdata.eye = dcm.Laterality
        # Patient ID
        imdata.patient_id = dcm.PatientID
        # image width
        imdata.width = dcm.Rows
        # image height
        imdata.height = dcm.Columns

        # store imdata
        output_data.append(imdata)

    return output_data

