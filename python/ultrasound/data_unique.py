# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 16:47:10 2019

@author: Diego Wanderley
@python: 3.6
@description: Delete unnecessary files
"""

import os

data_path = "//192.168.106.134/Diego Wanderley/Ultrasonix/organized/Data"

pnglist = [f[:-4] for f in os.listdir(data_path) if f.endswith('.png')]
xmllist = [f[:-4] for f in os.listdir(data_path) if f.endswith('.xml')]
#rflist = [f[:-3] for f in os.listdir(data_path) if f.endswith('.rf')]

# Unique documents            
docs = set(pnglist).symmetric_difference(xmllist)

for d in docs:
    path_xml = os.path.join(data_path, d + '.xml')
    path_rf = os.path.join(data_path, d + '.rf')
    os.remove(path_xml)
    os.remove(path_rf)
