import os
from io import BytesIO
from skimage import io
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import urllib.request
import urllib.parse
import mapbox_vector_tile
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
from PIL import Image as plimg
import numpy as np
from owslib.wms import WebMapService
from IPython.display import Image, display
import os
from layers import *
import time
 
overwrite = True
wms = ('')

#main is for testing 

#dates for certain layers may need to include T00:00:00Z

tcr = MODIS_Terra_CorrectedReflectance_TrueColor
vta = VIIRS_NOAA20_Thermal_Anomalies_375m_All

def main():
    dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]

    img = wms_params('2021-09-21T00:00:00Z', VIIRS_NOAA20_Thermal_Anomalies_375m_All)
    os.chdir('test_outs')
    out = open('VIIRS_NOAA20_Thermal_Anomalies_375m_All' + '.png', 'wb')
    out.write(img.read())
    out.close()
    Image('VIIRS_NOAA20_Thermal_Anomalies_375m_All' + '.png')


    #for d in dates:
        #img = wms_params(d, VIIRS_NOAA20_Thermal_Anomalies_375m_All)
        #out = open('VIIRS_NOAA20_Thermal_Anomalies_375m_All' + d + '.png', 'wb')
     
# create new directory
# Connect to GIBS WMS Service

def wms_params(timeP, layer):
    wms = WebMapService(layer["wms"])
    result = wms.getmap(layers= layer["layers"],  # Layers
                 srs=layer["crs"],  # Map projection
                 bbox=(layer["xmin"],layer["ymin"], layer["xmax"],layer["ymax"]),  # Bounds
                 size=layer["size"],  # Image size
                 time=timeP,  # Time of data
                 format=layer["format"],  # Image format
                 transparent=layer["transparent"])  # Nodata transparency
    return result




# Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
"""
img = wms.getmap(layers=['MODIS_Terra_CorrectedReflectance_TrueColor'],  # Layers
                 srs='epsg:4326',  # Map projection
                 bbox=(-180,-90,180,90),  # Bounds
                 size=(1200, 600),  # Image size
                 time='2021-09-21',  # Time of data
                 format='image/png',  # Image format
                 transparent=True)  # Nodata transparency
"""
# Save output PNG to a file
if __name__ == "__main__":
    main()