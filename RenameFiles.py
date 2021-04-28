# -*- coding: utf-8 -*-
"""
Created on Fri Apr 09 06:43:45 2021

@author: Steven Hill
"""

import os
path = 'F:/Astronomy/Projects/Planets/Jupiter/Imaging Data/20201009UT/'

fnlist = os.listdir(path)

for fn in fnlist:
    fnout=fn.replace("_Jupiter","-Jupiter")
    print fnout
    os.rename(path+fn,path+fnout)
    
