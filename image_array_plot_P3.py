# -*- coding: utf-8 -*-
"""
Created on Wed Oct 06 14:36:01 2021

@author: Steven Hill

PURPOSE:    Create arrays of images of planetary observations - the final
            navigated images for each filter channel plus a composite RGB
            image. This is a quick way to replace the image tables I'd 
            manually create in the annual Observations reports for each
            observing session.

EXAMPLE:    image_array_plot_P3("Jupiter","20210927UT")
"""

def image_array_plot_P3(target,obsdate):
    import sys
    drive='c:'
    sys.path.append(drive+'/Astronomy/Python Play')
    sys.path.append(drive+'/Astronomy/Python Play/Util_P3')
    sys.path.append(drive+'/Astronomy/Python Play/SpectroPhotometry/Spectroscopy')

    import os
    from matplotlib.pyplot import imread
    import pylab as pl
    
    ###########################################################################
    # Here's where we filter and select the images to plot. Probably want
    # more than one option, e.g.:
    #   - For posting to ALPO Japan or other public sites
    #   - For basic array of monchromatic derotated images, both with and 
    #     without wavelets processing
    #   - RGB array, e.g., RGB, 889-G-NUV, 656-647-632
    #   - Array corresponding to Maps presented for NH3 analysis
    ###########################################################################

    path='c:/Astronomy/Projects/Planets/'+target+'/Imaging Data/'+obsdate+'/'
    fnlist = os.listdir(path)
    #print fnlist
    pnglist=[k for k in fnlist if 'png' in k]
    #print pnglist
    derotated=[k for k in pnglist if 'Derot' in k]
    derotated=derotated+[k for k in pnglist if 'DR' in k]
    #print derotated
    wavelets=[k for k in derotated if 'Wavelets' in k]
    wavelets=wavelets+[k for k in derotated if 'WV' in k]
    print(wavelets)

    RGB=[k for k in pnglist if 'RGB' in k]
    print(RGB)
    print()
    waveletsRGB=[k for k in RGB if 'WhtBal-ClrSmth-Smth-Wavelets' in k]
    print("waveletsRGB=",waveletsRGB)
    
    filelist=wavelets+waveletsRGB

    nimages=len(filelist)
    
    print(nimages)
    print
    for i in range(0,nimages):
        print("filelist=",filelist[i])
    print()
    if nimages > 4:
        fig=pl.figure(figsize=(6.,6.), dpi=150, facecolor="black") #Landscape
        subx=3
        suby=3
    if nimages <=4:
        fig=pl.figure(figsize=(4.,4.), dpi=150, facecolor="black") #Landscape
        subx=2
        suby=2
    for i in range(1,nimages+1):
        print(filelist[i-1])
        #image=imread(path+filelist[i-1],flatten=False)
        tmp=load_png(path+filelist[i-1])
        image=tmp[:,:,0]
        ax=pl.subplot(subx,suby,i)
        ax.axis('off')
        ax.imshow(image,'gist_gray')
        pl.annotate(filelist[i-1][0:17],[0.02,0.93],color='white',
                    xycoords='axes fraction',fontsize=6)
        offset=len(target)+2
        pl.annotate(filelist[i-1][17+offset:23+offset],[0.7,0.93],color='white',
                    xycoords='axes fraction',fontsize=6)
    pl.subplots_adjust(left=0.00, bottom=0.0, right=1.0, top=1.0,
                wspace=0.001, hspace=0.001)

    pl.savefig(path+obsdate+target+"-NavigatedArray.png",dpi=300)
    
def load_png(file_path):
    """
    Purpose: Properly load a 48-bit PNG file
    Read from KITTI .png file
    Args:
        file_path string: file path(absolute)
    Returns:
        data (numpy.array): data of image in (Height, Width, 3) layout
    
    FROM: https://www.programcreek.com/python/example/98900/png.Reader
    """
    import png
    import numpy as np

    flow_object = png.Reader(filename=file_path)
    flow_direct = flow_object.asDirect()
    flow_data = list(flow_direct[2])
    (w, h) = flow_direct[3]['size']

    flow = np.zeros((h, w, 3), dtype=np.float64)
    for i in range(len(flow_data)):
        flow[i, :, 0] = flow_data[i][0::3]
        flow[i, :, 1] = flow_data[i][1::3]
        flow[i, :, 2] = flow_data[i][2::3]

    return flow.astype(np.uint16) 
