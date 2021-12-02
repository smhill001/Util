# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 10:57:55 2018
NAME:       ConfigFiles.py

PURPOSE:    This module provides a base class and various child classes for 
            setting up and drawing plots, including reading plot configuration
            files.
            
            0CLASS PlotSetup
            0  INIT
            0  loadplotparams
            0  Setup_Plot
            0  Setup_Caratopy_Map - NOTE SPELLING ERROR
            1Draw_with_Conf_Level

@author: Steven Hill
"""
import ConfigFiles as CF
drive='f:'

class PlotSetup(CF.readtextfilelines):
    """
    This class reads parameters from configuration files that determine how to
    set up various plots. It will also do the initial plot setup.
    """
    pass
    def loadplotparams(self,drive,PlotID,PlotType):
        #View has two options: raw or flux?

        self.ID=PlotID
        self.Type=PlotType

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            #print "fields[0]=",fields[0],PlotID
            if fields[0] == PlotID:
                #print "fields[1]=",fields[1],PlotType
                if fields[1] == PlotType:
                    self.PlotType=str(fields[1])
                    print self.PlotType,self.ID
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
                        #print fields[11],fields[13]
                        #print "###############",self.Labels
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

    def Setup_PlotDate(self,date_min,date_max,date_interval,
                       canvas_size=[6.5,2.5],new_canvas=True,subplot=[1,1,1]):
        import pylab as pl
        import numpy as np
        #SHOULD DECOUPLE FIGURE SIZE FROM PLOT SETUP, BUT PASS SUBPLOT LOC.
        if new_canvas:
            canvas=pl.figure(figsize=(canvas_size[0],canvas_size[1]), dpi=150, facecolor="white")
            canvas.subplots_adjust(hspace=0.001)
        AX=pl.subplot(subplot[0],subplot[1],subplot[2])
        #if self.Xtype=='linear':
        #    xtks=(date_max-date_min)/date_interval  
        #    pl.xticks(np.linspace(date_min,date_max,xtks, endpoint=True))
        #pl.xlim(date_min,date_max)
        if self.Ytype=='linear':
            ytks=(self.Y1-self.Y0)/self.DY+1  
            AX.set_yticks(np.linspace(self.Y0,self.Y1,ytks, endpoint=True))
        AX.set_ylim(self.Y0,self.Y1)
        AX.set_yscale(self.Ytype)
        AX.grid(linewidth=0.5)
        AX.tick_params(axis='both', which='major', labelsize=7)
        #IN THE FUTURE SHOULD MAKE THESE CONFIGURATION FILE FIELDS
        #if self.Type=="Time":
            #AX.set_ylabel(r"$TBD$",fontsize=7)
            #AX.set_xlabel(r"$TBD$",fontsize=7)
        #AX.set_title(self.ID,fontsize=9)
        return AX#,canvas
       
    def Setup_CaratoPy_Map(self,Projection,xs,ys,ns,xtk=True,ytk=True,ptitle=False):
        import pylab as pl
        import numpy as np
        import cartopy.crs as ccrs
        import matplotlib.path as mpath

        if Projection=="PC":
            self.ax = pl.subplot(xs,ys,ns,projection=ccrs.PlateCarree())
            self.ax.gridlines(crs=ccrs.PlateCarree(),linewidth=0.2)
            #ax.set_xticks(np.linspace(-180,180,13), minor=False, crs=None)
            self.ax.set_xticks(np.linspace(-180,180,13), minor=False, crs=None)
            self.ax.set_yticks(np.linspace(-90,90,7), minor=False, crs=None)
            if not(ytk):
                self.ax.set_yticklabels([])
            if ytk:
                pl.ylabel("Latitude (deg)",fontsize=7,labelpad=0.0)
            if not(xtk):
                self.ax.set_xticklabels([])
            if xtk:
                pl.xlabel("Longitude (deg)",fontsize=7,labelpad=0.0)
            self.ax.tick_params(axis='both', which='major', labelsize=7)
        else:
            if Projection=="NP":
                ax = pl.subplot(xs,ys,ns,projection=ccrs.NorthPolarStereo())
                ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
            elif Projection=="SP":
                ax = pl.subplot(xs,ys,ns,projection=ccrs.SouthPolarStereo())
                ax.set_extent([-180, 180, -90, 0], crs=ccrs.PlateCarree())
            ax.gridlines(crs=ccrs.PlateCarree(),linewidth=0.2)
            ax.set_xticks(np.linspace(-180,180,13), minor=False, crs=None)
            ax.set_yticks(np.linspace(-90,90,7), minor=False, crs=None)
            ax.tick_params(axis='both', which='major', labelsize=7)
            theta = np.linspace(0, 2*np.pi, 100)
            center, radius = [0.5, 0.5], 0.5
            verts = np.vstack([np.sin(theta), np.cos(theta)]).T
            circle = mpath.Path(verts * radius + center)
            ax.set_boundary(circle, transform=ax.transAxes)

        #IN THE FUTURE SHOULD MAKE THESE CONFIGURATION FILE FIELDS
        if not(ptitle):
            pl.title(self.ID,fontsize=7,pad=0.0)
        else:
            pl.title(ptitle,fontsize=7)
        
        return 0

    def Setup_SimpleCyl_Map(self,xs,ys,ns,xtk=True,ytk=True,ptitle=False):
        import pylab as pl
        import numpy as np
        import matplotlib.path as mpath

        self.ax = pl.subplot(xs,ys,ns)
        #self.ax.gridlines(linewidth=0.2)
        #ax.set_xticks(np.linspace(-180,180,13), minor=False, crs=None)
        self.ax.set_xticks(np.linspace(-180,180,13), minor=False)
        self.ax.set_yticks(np.linspace(-90,90,7), minor=False)
        if not(ytk):
            self.ax.set_yticklabels([])
        if ytk:
            pl.ylabel("Latitude (deg)",fontsize=7,labelpad=0.0)
        if not(xtk):
            self.ax.set_xticklabels([])
        if xtk:
            pl.xlabel("Longitude (deg)",fontsize=7,labelpad=0.0)
        self.ax.tick_params(axis='both', which='major', labelsize=7)

        #IN THE FUTURE SHOULD MAKE THESE CONFIGURATION FILE FIELDS
        if not(ptitle):
            pl.title(self.ID,fontsize=7,pad=0.0)
        else:
            pl.title(ptitle,fontsize=7)
        
        return 0


def Draw_with_Conf_Level(Data,scl,clr,lbl,step=False):                
    import pylab as pl
    if step:
        pl.step(Data[:,0],Data[:,1]*scl,label=lbl,linewidth=1.0,color=clr)
        if Data.shape[1]==4:
            pl.step(Data[:,0],(Data[:,1]+1.96*Data[:,3])*scl,linewidth=0.2,color=clr)
            pl.step(Data[:,0],(Data[:,1]-1.96*Data[:,3])*scl,linewidth=0.2,color=clr)
    else:
        pl.plot(Data[:,0],Data[:,1]*scl,label=lbl,linewidth=1.0,color=clr)
        if Data.shape[1]==4:
            pl.plot(Data[:,0],(Data[:,1]+1.96*Data[:,3])*scl,linewidth=0.2,color=clr)
            pl.plot(Data[:,0],(Data[:,1]-1.96*Data[:,3])*scl,linewidth=0.2,color=clr)
    #ax.fill_between((Data[:,0]),(Data[:,1]+1.96*Data[:,3])*scl,(Data[:,1]-1.96*Data[:,3])*scl)
    return 0        
