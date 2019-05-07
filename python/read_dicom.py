# -*- coding: utf-8 -*-
"""
Created on Tue May 07 16:43:40 2019

@author: Diego Wanderley
@python: 3.6
@description: Read DICOM files to save data on MongoDB Atlas.
"""


import os
import glob
import pydicom


class ImageData:
    '''Define Image Data class'''
    def __init__(self, uid, folder='./'):

        self.image_id = uid
        self.filename = uid + '.png'
        self.folder = folder
        self.path = folder + self.filename
        # Form information
        self.originalname = None
        self.date_acquisition = None
        self.date_upload = None      
        self.observations = None   # Text field
        self.patientId = None      # Text field   
        self.eye = None            # Text field   
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


# Root directory
I_DIR = '../images'
# Set of files
DICOM_LIST = (glob.glob(os.path.join(I_DIR + '/', '*.dcm')))


for dcm_str in DICOM_LIST:

    dcm = pydicom.dcmread(dcm_str)
    uid = dcm.SOPInstanceUID
    imdata = ImageData(uid=uid)

    imdata.eye = dcm.Laterality
    imdata.patientId = dcm.PatientID
    imdata.width = dcm.Rows
    imdata.heigth = dcm.Columns
    print(imdata)
