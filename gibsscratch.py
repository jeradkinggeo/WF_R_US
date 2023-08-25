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
import os as os
from layers import MODIS_Terra_CorrectedReflectance_TrueColor
overwrite = True
wms = ('')

def main():
    dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]

    img = wms_params('2021-09-21', MODIS_Terra_CorrectedReflectance_TrueColor)
    os.chdir('test_outs')

    for d in dates:
        img = wms_params(d, MODIS_Terra_CorrectedReflectance_TrueColor)
        out = open('MODIS_Terra_CorrectedReflectance_TrueColor' + d + '.png', 'wb')
        out.write(img.read())
        out.close()
        Image('MODIS_Terra_CorrectedReflectance_TrueColor' + d + '.png')


# create new directory
# Connect to GIBS WMS Service

def wms_params(timeP, layer):
    wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?')
    img = wms.getmap(layers= layer["layers"],  # Layers
                 srs=layer["crs"],  # Map projection
                 bbox=(layer["xmin"],layer["ymin"], layer["xmax"],layer["ymax"]),  # Bounds
                 size=layer["size"],  # Image size
                 time=timeP,  # Time of data
                 format=layer["format"],  # Image format
                 transparent=layer["transparent"])  # Nodata transparency
    return img




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