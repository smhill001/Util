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
            #print fields[0], fields[1]
            if fields[0] == TargetID:
                self.TargetID=fields[0]
                self.TargetType=fields[1]
                self.RA2000=float(fields[2])
                self.DE2000=float(fields[3])
                self.Distance=float(fields[4])
                self.DistUnits=fields[5]
                if self.TargetType=="Stars":
                    self.mV=float(fields[6])
                    self.SpecType=fields[7]
                elif self.TargetType=="Galaxies":
                    self.PA=float(fields[6])
                    self.Incl=float(fields[7])
                    self.AppSize=float(fields[8])

class built_path:
    def __init__(self,TargetParams):
        self.drive="f:"
        self.base_path='/Astronomy/Projects/'
        self.base_path=self.drive+self.base_path+TargetParams.TargetType+'/'+TargetParams.TargetID+'/'
        
    def spectra(self,dateUT):
        self.input_path=self.base_path+'Spectral Data/'+dateUT+'/'
        self.output_path=self.base_path+'Spectral Data/1D Spectra/'
        self.config_path=self.base_path+'Spectral Data/1D Spectra/Configuration Files/'
        self.reference_path=self.drive+'/Astronomy/Python Play/SPLibraries/SpectralReferenceFiles/ReferenceLibrary/'
        
    def Equivalent_Width(self):
        self.input_path=self.base_path+'Spectral Data/1D Spectra/'
        self.output_path=self.base_path+'Spectral Data/EWs/'