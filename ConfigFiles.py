# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 10:57:55 2018

@author: Steven Hill
"""

drive='f:'

class readtextfilelines:
    def __init__(self,FiletoRead):
        #Read ALL records in a text file. No path info is needed because
        #  it reads from the working directory. This may or may not be
        #  a good general working assumption.
        CfgFile=open(FiletoRead,'r')
        self.CfgLines=CfgFile.readlines()
        CfgFile.close()
        self.nrecords=len(self.CfgLines)
        self.FiletoRead=FiletoRead
        
        
class PlotSetup(readtextfilelines):
    """
    This class builds on the readtextfilelines class to add parameters 
    for setting up plots. It will also do the initial plot setup.
    
    SMH 6/7/18
    """
    pass
    def loadplotparams(self,drive,PlotID,PlotType):
        #View has two options: raw or flux?

        self.ID=PlotID

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            #print fields[0], fields[1]
            if fields[0] == PlotID:
                if fields[1] == PlotType:
                    #print "In first if, fields[1]",fields[:]
                    self.PlotType=str(fields[1])
                    self.X0=float(fields[2])
                    self.X1=float(fields[3])
                    self.DX=float(fields[4])
                    self.Xtype=str(fields[5])
                    self.Y0=float(fields[6])
                    self.Y1=float(fields[7])
                    self.DY=float(fields[8])
                    self.Ytype=str(fields[9])
                    self.DataFile=str(fields[10])

    def Setup_Plot(self):
        import pylab as pl
        import numpy as np
        #SHOULD DECOUPLE FIGURE SIZE FROM PLOT SETUP, BUT PASS SUBPLOT LOC.
        pl.figure(figsize=(6.5, 2.5), dpi=150, facecolor="white")
        pl.subplot(1, 1, 1)
        
        xtks=(self.X1-self.X0)/self.DX+1       
        pl.xlim(self.X0,self.X1)
        pl.xticks(np.linspace(self.X0,self.X1,xtks, endpoint=True))
        
        ytks=(self.Y1-self.Y0)/self.DY+1       
        pl.ylim(self.Y0,self.Y1)
        pl.yticks(np.linspace(self.Y0,self.Y1,ytks, endpoint=True))
        pl.yscale(self.Ytype)
        
        pl.grid()
        pl.tick_params(axis='both', which='major', labelsize=7)
        #IN THE FUTURE SHOULD MAKE THESE CONFIGURATION FILE FIELDS
        pl.ylabel(r"$Normalized$ $Response$",fontsize=7)
        pl.xlabel(r"$Wavelength (nm)$",fontsize=7)
        pl.title("Normalized Response",fontsize=9)
        
        return 0
