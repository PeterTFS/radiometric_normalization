from radiometric_normalization.wrappers import pif_wrapper
from radiometric_normalization.wrappers import transformation_wrapper
from radiometric_normalization.wrappers import normalize_wrapper
from radiometric_normalization import gimage
from radiometric_normalization import pif

## OPTIONAL

import logging
import numpy
import subprocess
from osgeo import gdal
from radiometric_normalization.wrappers import display_wrapper
import os

logging.basicConfig(level=logging.DEBUG)
##

## OPTIONAL - Cut dataset to colocated sub scenes and create and BGRN image
# LC08_L1TP_044034_20170105_20170218_01_T1 is the older scene and so it is set as the reference.
# Need to check the band mapping for the Sentinel 2 (S2A ?S2B)
band_mapping = [{'name': 'blue', 'S2': 'B2'}, {'name': 'green', 'S2':'B3'}, {'name': 'red', 'S2': 'B4'}, {'name': 'nir', 'S2': 'B8'}]
#get the list of band name for sentinel-2 from 
"""
  Band_1=Blue
  Band_10=SWIR2
  Band_2=Green
  Band_3=Red
  Band_4=RedEdge705
  Band_5=RedEdge740
  Band_6=RedEdge783
  Band_7=NIR
  Band_8=NarrowNIR
  Band_9=SWIR1
"""
WorkSpace = os.chdir(r'C:\\DEV\\FuelMapping\\registration\\Multiband_Images')
#full_candidate_basename = 'LC08_L1TP_044034_20170427_20170428_01_RT'
full_candidate_name = 'S2A_MSIL2A_T14RPV_N0205_20170430_10m.tif'
#Analyze the file name for image to process 
# e.g. S2B_MSIL2A_T14RMT_N0205_20171022_10m
# e.g. S2A_MSIL2A_T14RMT_N0205_20170430_10m

#full_reference_basename = 'LC08_L1TP_044034_20170105_20170218_01_T1'
full_reference_name = 'S2A_MSIL2A_T14RPV_N0205_20170507_10m'
"""
candidate_basename = 'candidate'
reference_basename = 'reference'
full_candidate_filenames = ['{}_{}.TIF'.format(full_candidate_basename, b['S2']) for b in band_mapping]
print full_candidate_filenames
candidate_filenames = ['{}_{}.TIF'.format(candidate_basename, b['name']) for b in band_mapping]
print candidate_filenames

full_reference_filenames = ['{}_{}.TIF'.format(full_reference_basename, b['S2']) for b in band_mapping]
reference_filenames = ['{}_{}.TIF'.format(reference_basename, b['name']) for b in band_mapping]

for full_filename, cropped_filename in zip(full_candidate_filenames, candidate_filenames):
    print full_filename,cropped_filename
    #subprocess.check_call(['gdal_translate', '-projwin', '545000', '4136000', '601000', '4084000', full_filename, cropped_filename])
    #subprocess.check_call(["c:\Program Files\QGIS 2.18\bin\gdal_translate.exe", '-projwin', '600000', '3500040', '709800', '3390240', full_filename, cropped_filename])

# for full_filename, cropped_filename in zip(full_reference_filenames, reference_filenames):
#     subprocess.check_call(["c:\Program Files\QGIS 2.18\bin\gdal_translate.exe", '-projwin', '545000', '4136000', '601000', '4084000', full_filename, cropped_filename])

band_gimgs = {}
for cropped_filename in candidate_filenames:
    print cropped_filename
    band = cropped_filename.split('_')[1].split('.TIF')[0]
    print band

    # band_gimgs[band] = gimage.load(cropped_filename)
cropped_filename = "S2A_MSIL2A_T14RPV_N0205_20170507_10m.tif"
band_gimgs = gimage.load(cropped_filename)
print band_gimgs

candidate_path = 'candidate.tif'
combined_alpha = numpy.logical_and.reduce([b.alpha for b in band_gimgs.values()])
combined_alpha = [1,2,3,7]
print combined_alpha

temporary_gimg = gimage.GImage([band_gimgs[b].bands[0] for b in ['blue', 'green', 'red', 'nir']], combined_alpha, band_gimgs['blue'].metadata)
gimage.save(temporary_gimg, candidate_path)

band_gimgs = {}
for cropped_filename in reference_filenames:
    band = cropped_filename.split('_')[1].split('.TIF')[0]
    band_gimgs[band] = gimage.load(cropped_filename)

reference_path = 'reference.tif'
combined_alpha = numpy.logical_and.reduce([b.alpha for b in band_gimgs.values()])
temporary_gimg = gimage.GImage([band_gimgs[b].bands[0] for b in ['blue', 'green', 'red', 'nir']], combined_alpha, band_gimgs['blue'].metadata)
gimage.save(temporary_gimg, reference_path)
##
"""
#candidate_path = os.path.join(WorkSpace, full_candidate_name)
candidate_path = r'C:\\DEV\\FuelMapping\\registration\\Multiband_Images\\S2A_MSIL2A_T14RPV_N0205_20170430_10m_3bands.tif'
#reference_path = os.path.join(WorkSpace, full_reference_name)
reference_path = r'C:\\DEV\\FuelMapping\\registration\\Multiband_Images\\S2A_MSIL2A_T14RPV_N0205_20170507_10m_3bands.tif'
print candidate_path,reference_path
parameters = pif.pca_options(threshold=100)
combined_alpha = [1, 2, 3, 7]
pif_mask = pif_wrapper.generate(candidate_path, reference_path, method='filter_PCA', last_band_alpha=False, method_options=parameters)


## OPTIONAL - Save out the PIF mask
candidate_ds = gdal.Open(candidate_path)
metadata = gimage.read_metadata(candidate_ds)
print metadata
pif_gimg = gimage.GImage([pif_mask], numpy.ones(pif_mask.shape, dtype=numpy.bool), metadata)
# gimage.save(pif_gimg, 'PIF_pixels_3bands.tif')

##

# transformations = transformation_wrapper.generate(candidate_path, reference_path, pif_mask, method='linear_relationship', last_band_alpha=True)
transformations = transformation_wrapper.generate(candidate_path, reference_path, pif_mask, method='linear_relationship', last_band_alpha=False)
## OPTIONAL - View the transformations
print transformations
##

# normalised_gimg = normalize_wrapper.generate(candidate_path, transformations, last_band_alpha=True)
normalised_gimg = normalize_wrapper.generate(candidate_path, transformations, last_band_alpha=False)
result_path = 'S2A_MSIL2A_T14RPV_N0205_20170430_10m_3bands_normalized.tif'
# gimage.save(normalised_gimg, result_path)


## OPTIONAL - View the effect on the pixels (SLOW)
from radiometric_normalization.wrappers import display_wrapper
display_wrapper.create_pixel_plots(candidate_path, reference_path, 'Original', limits=[0, 30000], last_band_alpha=False)
display_wrapper.create_pixel_plots(result_path, reference_path, 'Transformed', limits=[
                                   0, 30000], last_band_alpha=False)
display_wrapper.create_all_bands_histograms(
    candidate_path, reference_path, 'Original', x_limits=[4000, 25000], last_band_alpha=False)
display_wrapper.create_all_bands_histograms(
    result_path, reference_path, 'Transformed', x_limits=[4000, 25000], last_band_alpha=False)
##

