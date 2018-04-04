# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 16:20:15 2018

@author: pyang
"""
from geoarray import GeoArray
from arosics import COREG
#print(dir(GeoArray))
#im_reference = r'C:\DEV\FuelMapping\Arc_Version_Test\Hill_Country_Pilot\AC_Images\S2A_MSIL2A_20170130T171541_N0204_R112_T14RMT_20170130T171741.SAFE\GRANULE\L2A_T14RMT_A008403_20170130T171541\IMG_DATA\R10m\L2A_T14RMT_20170130T171541_B02_10m.jp2'
#im_reference = r'C:\DEV\FuelMapping\registration\Sample_Images\L2A_T14RMT_20170430T171301_B04_10m__shifted_to__L2A_T14RMT_20171022T171339_B04_10m.tif'
#im_target    = '/path/to/your/tgt_image.bsq'
im_reference = r'c:\DEV\FuelMapping\registration\Multiband_Images\S2B_MSIL2A_T14RMT_N0205_20171022_10m.tif'
geoArr  = GeoArray(im_reference)
#print(help(geoArr))
#CR = COREG(im_reference, im_target, wp=(354223, 5805559), ws=(256,256))
#CR.calculate_spatial_shifts()
#for single band image
#im_reference = r'C:\DEV\FuelMapping\registration\Sample_Images\L2A_T14RMT_20171022T171339_B04_10m.jp2'
#im_target = r'C:\DEV\FuelMapping\registration\Sample_Images\L2A_T14RMT_20170430T171301_B04_10m.jp2'
#shiftedfn = im_target[0:-4] + "_pyshifted"  + '.tif'
#print(shiftedfn)
##print(help(CRL.correct_shifts()))
#for full band image
#im_reference = r'c:\DEV\FuelMapping\registration\Multiband_Images\S2B_MSIL2A_T14RMT_N0205_20171022_10m.tif'
#im_target = r'c:\DEV\FuelMapping\registration\Multiband_Images\S2A_MSIL2A_T14RMT_N0205_20170430_10m.tif'
#shiftedfn = im_target[0:-4] + "_pyfullbandshifted"  + '.tif'
#CRL = COREG(im_reference,im_target,shiftedfn,fmt_out='GTiff')
#CRL.correct_shifts()
#shiftedarray.save(shiftedfn,fmt='GTiff',creationOptions="WRITE_METADATA=YES")
#
#import gdal
#print(help(gdal))
#Local 
from arosics import COREG_LOCAL 
im_reference = r'C:\DEV\FuelMapping\registration\Sample_Images\L2A_T14RMT_20171022T171339_B04_10m.jp2'
im_target = r'C:\DEV\FuelMapping\registration\Sample_Images\L2A_T14RMT_20170430T171301_B04_10m.jp2'
shiftedfn = im_target[0:-4] + "_pylocalshifted"  + '.tif'
kwargs = {
    'path_out':shiftedfn,
    'fmt_out':'GTiff',
    'grid_res'     : 200,
    'window_size'  : (64,64),
    'q'            : False,
}

CRL = COREG_LOCAL(im_reference,im_target,**kwargs)
CRL.correct_shifts()
