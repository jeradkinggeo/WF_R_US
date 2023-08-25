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

    img = wms_req('2021-09-21', VIIRS_NOAA20_Thermal_Anomalies_375m_All)
    print(img)
    time.sleep(5)
    os.chdir('test_outs')
    out = open('vta_test' + '.png', 'wb')
    out.write(img.read())
    out.close()
    Image('vta_test' + '.png')


    #for d in dates:
        #img = wms_params(d, VIIRS_NOAA20_Thermal_Anomalies_375m_All)
        #out = open('VIIRS_NOAA20_Thermal_Anomalies_375m_All' + d + '.png', 'wb')
     
# create new directory
# Connect to GIBS WMS Service

#Current version of wms_params takes the name of the layer to check format of time
def wms_req(timeP, layer):
    if layer == MODIS_Terra_CorrectedReflectance_TrueColor:
        wms = WebMapService(layer["wms"])
        result = wms.getmap(layers= layer["layer"],  # Layers
                    srs=layer["crs"],  # Map projection
                    bbox=(layer["xmin"],layer["ymin"], layer["xmax"],layer["ymax"]),  # Bounds
                    size=layer["size"],  # Image size
                    time=timeP,  # Time of data
                    format=layer["format"],  # Image format
                    transparent=layer["transparent"])
        return result
    elif layer == VIIRS_NOAA20_Thermal_Anomalies_375m_All:
        wms = WebMapService(layer["wms"])
        result = wms.getmap(layers= layer["layer"],  # Layers
                    srs=layer["crs"],  # Map projection
                    bbox=(layer["xmin"],layer["ymin"], layer["xmax"],layer["ymax"]),  # Bounds
                    size=layer["size"],  # Image size
                    time=timeP + "T00:00:00Z",  # Time of data and print it
                    format=layer["format"],  # Image format
                    transparent=layer["transparent"])
        return result
    else:
        print("Layer not found")
        return None




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