# -*- coding: utf-8 -*-
"""
Created on Fri Apr 09 06:43:45 2021

@author: Steven Hill
"""

str_in="20220124UT"
str_out="20220131UT"
#path = 'F:/Astronomy/Projects/Planets/Jupiter/Imaging Data/20201009UT/'
#path='F:/Astronomy/Data/2021/10/12UT/M27/raw/'

path="c:/Astronomy/Data/2022/01/31UT/"
def RenameFiles(path,str_in,str_out):
    import os
    fnlist = os.listdir(path)
    print(fnlist)
    for fn in fnlist:
        print(fn)
        fnout=fn.replace(str_in,str_out)
        print(fnout)
        os.rename(path+fn,path+fnout)
    
def MaximDL2WinJUPOS_Filenames(path):
    """
    PURPOSE: To create WinJUPOS conforming file names from FITS planetary image
             sequences taken with MaximDL.
    """
    import os
    from astropy.io import fits

    fnlist = os.listdir(path)
    print(fnlist)
    FITSlist=[k for k in fnlist if 'fit' in k]
    #print FITSlist
    for fn in FITSlist:
        hdulist=fits.open(path+fn)
        header=hdulist[0].header

        fnout=header["DATE-OBS"][0:10]+"-"+header["DATE-OBS"][11:13]+\
              header["DATE-OBS"][14:16]+"_"+str(int(header["DATE-OBS"][17:19])/6)+\
              "-Jupiter_"+header["FILTER"]+".fit"
        hdulist.close()
        print(fn,fnout)
        os.rename(path+fn,path+fnout)
 