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
import layersclass as lc
import time
 
overwrite = True
wms = ('')

#main is for testing 

#dates for certain layers may need to include T00:00:00Z
test = lc.MODIS_Terra_CorrectedReflectance_TrueColor

lc.MODIS_Terra_CorrectedReflectance_TrueColor.wms_req('2021-09-21')


#Line 42, cannot concatenate str and list

def main():
    lc.MODIS_Terra_CorrectedReflectance_TrueColor.wms_req('2021-09-21')
    #Print on of the layers from layerclass.py
    #lc.wms_req('2021-09-21', tcr)

#    dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]
#    print(os.getcwd())
#    os.chdir('test_outs')
#    for sat in layers:  
#        for d in dates:
#            img = wms_req(d, sat)  
#            with open(sat[layers] + d + '.png', 'wb') as out:
#                out.write(img.read())
#                print(os.getcwd())

    #out = open('vta_test' + '.png', 'wb')
    #out.write(img.read())
    #out.close()
    #Image('vta_test' + '.png')

#Current version of wms_params takes the name of the layer to check format of time

def wms_req(timeP, layer):
    if layer["Time_format"] == True:
        timeP = timeP + "T00:00:00Z"
    wms = WebMapService(layer["wms"])
    result = wms.getmap(layers= layer["layer"],  # Layers
                srs=layer["crs"],  # Map projection
                bbox=(layer["xmin"],layer["ymin"], layer["xmax"],layer["ymax"]),  # Bounds
                size=layer["size"],  # Image size
                time=timeP,  # Time of data
                format=layer["format"],  # Image format
                transparent=layer["transparent"])
    return result


#This doesnt work yet
def imgdir_make(satname, date, region):
    #check if date is a list
    if isinstance(date, list):
        dates = date
        for d in dates:
            pathname = region + '_' + dates
    if os.path.exists(pathname):
        print(pathname + "Directory already exists, overwrite? (y/n)")
        if input() == 'y':
            os.makedirs(pathname)
            os.chdir(pathname)
        else:
            print("Aborting")
    else:
        os.makedirs(pathname)
        os.chdir(pathname)
        #create subdirectories for each satellite
        for sat in satname:
            os.makedirs(sat)
            os.chdir(sat)
            os.chdir('..')

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