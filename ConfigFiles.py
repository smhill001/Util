# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 10:57:55 2018

@author: Steven Hill
"""

drive='f:'

class readtextfilelines:
    def __init__(self,FiletoRead):
        #print "readtextfilelines, FiletoRead:",FiletoRead
        #Read ALL records in a text file. No path info is needed because
        #  it reads from the working directory. This may or may not be
        #  a good general working assumption.
        CfgFile=open(FiletoRead,'r')
        self.CfgLines=CfgFile.readlines()
        CfgFile.close()
        self.nrecords=len(self.CfgLines)
        self.FiletoRead=FiletoRead
        print "Hi end of readtextfilelines"
        
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
        self.Type=PlotType

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            print "************",fields[0],fields[1],fields[13]
            if fields[0] == PlotID:
                if fields[1] == PlotType:
                    print "In first if, fields[1]",fields[:]
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
                if self.PlotType=="Map":
                    self.Labels=str(fields[11])
                    print fields[11]
                    print "###############",self.Labels
                    self.Grid=str(fields[12])
                    self.ColorPlane=str(fields[13])

    def Setup_Plot(self):
        import pylab as pl
        import numpy as np
        #SHOULD DECOUPLE FIGURE SIZE FROM PLOT SETUP, BUT PASS SUBPLOT LOC.
        pl.figure(figsize=(6.5, 2.5), dpi=150, facecolor="white")
        pl.subplot(1, 1, 1)
        if self.Xtype=='linear':
            xtks=(self.X1-self.X0)/self.DX+1  
            pl.xticks(np.linspace(self.X0,self.X1,xtks, endpoint=True))
        pl.xlim(self.X0,self.X1)
        if self.Ytype=='linear':
            ytks=(self.Y1-self.Y0)/self.DY+1  
            pl.yticks(np.linspace(self.Y0,self.Y1,ytks, endpoint=True))
        pl.ylim(self.Y0,self.Y1)
        pl.yscale(self.Ytype)
        pl.grid()
        pl.tick_params(axis='both', which='major', labelsize=7)
        #IN THE FUTURE SHOULD MAKE THESE CONFIGURATION FILE FIELDS
        if self.Type=="Spectra":
            pl.ylabel(r"$Counts-s^{-1}$-$m^{-2}$-$nm^{-1}$",fontsize=7)
            pl.xlabel(r"$Wavelength (nm)$",fontsize=7)
        if self.Type=="Response":
            pl.ylabel(r"$Normalized$ $Response$",fontsize=7)
            pl.xlabel(r"$Wavelength (nm)$",fontsize=7)
        elif self.Type=="Belt":
            pl.ylabel("Latitude (deg)")
            pl.xlabel("Year",fontsize=7)
        pl.title(self.ID,fontsize=9)
        
        return 0
    
    def Setup_Map(self):
        import pylab as pl
        import numpy as np
        #SHOULD DECOUPLE FIGURE SIZE FROM PLOT SETUP, BUT PASS SUBPLOT LOC.
        pl.figure(figsize=(6.0, 3.0), dpi=150, facecolor="white")
        pl.subplot(1, 1, 1)
        #Calculate scaling - remember X0 is left side of plot, X1 is extent
        Xpix0=0;Xpix1=self.X1-1
        Xtickspix=(self.X1)/self.DX
        DXpix=(Xpix1)/Xtickspix
        pl.xticks(np.arange(Xpix0,Xpix1+1,DXpix),np.mod(np.arange(540,179,-30),360))
        #Need to figure out the labeling for less the 360 longitude
        #pl.xticks(np.arange(Xpix0,Xpix1+1,DXpix),np.mod(np.arange(540,179,-30),360))
        #Calculate scaling
        Ypix0=0;Ypix1=self.Y1-self.Y0-1
        Ytickspix=(self.Y1-self.Y0)/self.DY
        DYpix=(Ypix1-Ypix0)/Ytickspix
        pl.yticks(np.arange(Ypix0,Ypix1+1,DYpix),np.arange(self.Y1,self.Y0-1,-self.DY))
        print self.Y1, self.Y0-1, self.DY
        print "Ypix0,Ypix1,Ytickspix,DYpix=",Ypix0,Ypix1,Ytickspix,DYpix
        print np.arange(Ypix0,Ypix1+1,DYpix)
        print np.arange(self.Y1,self.Y0-1,-self.DY)
        print np.arange(0,181,30)
        if self.Labels=="True": pl.grid(linewidth=0.2)
        print "********************",self.Labels
        pl.tick_params(axis='both', which='major', labelsize=7)
        #IN THE FUTURE SHOULD MAKE THESE CONFIGURATION FILE FIELDS
        if self.Type=="Map":
            pl.ylabel("Latitude (deg)",fontsize=7)
            pl.xlabel("Longitude (deg)",fontsize=7)
        pl.title(self.ID,fontsize=9)
        
        return 0

class Target_Parameters(readtextfilelines):
    """
    This class builds on the base class to add parameters specific to
    galaxies: position angle, inclination, and classification. Note that
    for other deep sky objects, in particular planetary nebulae, the 
    parameters would be identical or mostly identical. 
    
    SMH 1/11/18
    """
    pass
    def loadtargetparams(self,TargetID):
        #View has two options: raw or flux?
        #Test_plot_params_base.__init__(self,drive,ObjIdentifierDD)
        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            #print fields[0], fields[1]
            if fields[0] == TargetID:
                print "In first if, fields[1]",fields[:]
                #self.TargetType=str(fields[1])
                self.TargetID=fields[0]
                self.TargetType=fields[1]
                self.RA2000=float(fields[2])
                self.DE2000=float(fields[3])
                self.Distance=float(fields[4])
                self.DistUnits=fields[5]
                self.mV=float(fields[6])
                self.SpecType=fields[7]

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