# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 10:56:15 2019

@author: Diego Wanderley
@python: 3.6
@description: Rearrange folders of ultrasound data
"""

import os
import shutil
import xmltodict

input_folder = "//192.168.106.134/Diego Wanderley/Ultrasonix/filtered_data"
output_folder = "//192.168.106.134/Diego Wanderley/Ultrasonix/organized"

# Get internal folders (by patient ID)
folders_in = os.listdir(input_folder)
# Read content
for pat_id in folders_in:
    # Full path
    pat_path = os.path.join(input_folder, pat_id)
    # Get list of exames
    folders_pat = os.listdir(pat_path)
    # Read patient folders
    for pat_exm in folders_pat:
        if pat_exm == 'patient.xml':
            # Read patient data (XML)
            pat_xml = os.path.join(pat_path, 'patient.xml')
            pat_xml_out = os.path.join(output_folder + "/Patients", pat_id + ".xml")
            shutil.copy(pat_xml, pat_xml_out)
            """
            doc = None
            with open(pat_xml) as fd:
                doc = xmltodict.parse(fd.read())
            """
            # DO SOMETHING WITH DOC/Patinet XML
        else:
            # Read patient exames (by date)
            exam_path = os.path.join(pat_path, pat_exm)
            # Get list of documents
            pnglist = [f[:8] for f in os.listdir(exam_path) if f.endswith('.png')]
            xmllist = [f[:8] for f in os.listdir(exam_path) if f.endswith('.xml')]
            # Unique documents            
            docs = set(pnglist).intersection(xmllist)
            # Read each file
            for d in docs:
                # New name and output path (without extensions)
                new_name = 'pat_' + pat_id + '_' + \
                    pat_exm[6:10] + pat_exm[0:2] + pat_exm[3:5] + \
                    '_' + d[0:2] + d[3:5] + d[6:8]
                path_out = os.path.join(output_folder + "/Data", new_name)
                
                # Full path of each file
                path_png = os.path.join(exam_path, d + '.png')
                path_xml = os.path.join(exam_path, d + '.png.xml')
                path_rf = os.path.join(exam_path, d + '.rf')

                # Copy and rename
                shutil.copy(path_png, path_out + ".png")
                shutil.copy(path_xml, path_out + ".xml")
                shutil.copy(path_rf, path_out + ".rf")
                '''
                ex_doc = None
                with open(path_xml) as fd:
                    ex_doc = xmltodict.parse(fd.read())
                '''

                print('')

