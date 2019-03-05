# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 10:57:55 2018

NAME:       ConfigFiles.py

PURPOSE:    This module provides a base class and various child classes for 
            reading and parsing comma-delimited text configuration files. 
            The base class could also be extended for reading data files.
            
            0CLASS readtextfilelines
            0  INIT
            1CLASS Target_Parameters
            1  INIT
            1  loadtargetparams
            2CLASS built_path
            2  INIT
            2  Spectra
            2  Equivalent_Width

@author: Steven Hill
"""

drive='f:'

class readtextfilelines:
    def __init__(self,FiletoRead):
        """
        If no path is given, this class reads from the working directory.
        """
        CfgFile=open(FiletoRead,'r')
        self.CfgLines=CfgFile.readlines()
        CfgFile.close()
        self.nrecords=len(self.CfgLines)
        self.FiletoRead=FiletoRead
        print "Read "+str(self.nrecords)+" records"

class Target_Parameters(readtextfilelines):
    """
    This class reads target attribute parameters. It is aimed at deep sky
    objects such as galaxies: position angle, inclination, and classification.  
    """
    pass
    def loadtargetparams(self,TargetID):

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            print fields[0], fields[1]
            if fields[0] == TargetID:
                self.TargetID=fields[0]
                self.TargetType=fields[1]
                self.RA2000=float(fields[2])
                self.DE2000=float(fields[3])
                self.Distance=float(fields[4])
                self.DistUnits=fields[5]
                if self.TargetType=="Stars" or self.TargetType=="Planets":
                    self.mV=float(fields[6])
                    self.SpecType=fields[7]
                elif self.TargetType=="Galaxies":
                    self.PA=float(fields[6])
                    self.Incl=float(fields[7])
                    self.AppSize=float(fields[8])

class measurement_list(readtextfilelines):
    #Used to reside in SRL and have a different API for loading records
    pass
    
    def load_records(self,MeasTgt="All",DateUTSelect="All",Grating="All"):

        print "Hi in measurement_list>load_records"
        self.MeasTarget=[]  #Keyword for star identification
        self.DataType=[]           #Target, e.g., component of a multiple star
        self.DataTarget=[]           #Target, e.g., component of a multiple star
        self.DateUT=[]           #UT Date of observation: YYYYMMDDUT
        self.Optics=[]       #Instrument code, to be used for aperture
        self.Camera=[]       #Instrument code, to be used for aperture
        self.Grating=[]    #Grating 100lpm or 200lpm or None
        self.FileList=[]         #List of observation image files (FITS)
        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            if MeasTgt=="All" or MeasTgt==str(fields[0]):
                if Grating=="All" or Grating==str(fields[6]):
                    if DateUTSelect=="All" or DateUTSelect==str(fields[3]):
                        self.MeasTarget.extend([str(fields[0])])
                        self.DataType.extend([str(fields[1])])
                        self.DataTarget.extend([str(fields[2])])
                        self.DateUT.extend([str(fields[3])])
                        self.Optics.extend([str(fields[4])])
                        self.Camera.extend([str(fields[5])])
                        self.Grating.extend([str(fields[6])])
                        self.FileList.extend([str(fields[7])])

class ObsFileNames(readtextfilelines):
    #Used to be the function GetObsFileNames in SRL
    pass
    def GetFileNames(self):
        self.FNArray=[]
        for recordindex in range(0,self.nrecords):
            fields=str(self.CfgLines[recordindex]).split(',')
            self.FNArray.append(fields[0])

class built_path:
    def __init__(self,TargetParams):
        self.drive="f:"
        self.base_path='/Astronomy/Projects/'
        self.base_path=self.drive+self.base_path+TargetParams.TargetType+'/'+TargetParams.TargetID+'/'
        
    def spectra(self,dateUT):
        self.input_path=self.base_path+'Spectral Data/'+dateUT+'/'
        self.One_D_path=self.base_path+'Spectral Data/1D Spectra/'
        self.EW_path=self.base_path+'Spectral Data/EWs/'
        self.config_path=self.base_path+'Spectral Data/1D Spectra/Configuration Files/'
        self.reference_path=self.drive+'/Astronomy/Python Play/SPLibraries/SpectralReferenceFiles/ReferenceLibrary/'
        
    def Equivalent_Width(self):
        self.input_path=self.base_path+'Spectral Data/1D Spectra/'
        self.output_path=self.base_path+'Spectral Data/EWs/'
        
def MakeKeyDate(FN):
    import datetime

    Key=FN[0:7]+FN[16:32]
    DateTime=datetime.datetime.strptime(Key[7:11]+"-"+Key[11:13]+"-" \
        +Key[13:15]+"T"+Key[15:17]+":"+Key[17:19]+":"+Key[19:21], \
        '%Y-%m-%dT%H:%M:%S')

    return Key,DateTime
