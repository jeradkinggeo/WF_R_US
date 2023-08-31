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

#def main():
#    satlist = [lc.MODIS_Terra_CorrectedReflectance_TrueColor, lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All]
#    dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]
#    imgdir_make(satlist, dates[1::], 'World')

def main():
    wmsUrl = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
    SERVICE=WMS&REQUEST=GetCapabilities'
    response = requests.get(wmsUrl)
    WmsXml = xmltree.fromstring(response.content)
    print(xmltree.tostring(WmsXml, pretty_print = True, encoding = str))
    os.mkdir('WMS_Response_capabilities')
    os.chdir('WMS_Response_capabilities')
    with open('WMS_Response_capabilities.xml', 'wb') as file:
        file.write(response.content)



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


def imgdir_make(satname, date, region):
    sat = satname
    if isinstance(date, list) and isinstance(satname, list):
        dates = date
        pri_dir = "Image Directory"
        os.makedirs(pri_dir)
        os.chdir(pri_dir)
        for d in range(0, len(dates)):
            pathname = region + '_' + dates[d]
            os.makedirs(pathname)
            os.chdir(pathname)
            for s in range(0, len(satname)):
                img = satname[s].wms_req(dates[d])
                with open(satname[s].abr + "_" + dates[d] + '.png', 'wb') as out:
                    out.write(img.read())
            os.chdir('..')      
    elif isinstance(date, list):
        dates = date
        pri_dir = "Image Directory"
        os.makedirs(pri_dir)
        os.chdir(pri_dir)
        for d in range(0, len(dates)):
            pathname = region + '_' + dates[d]
            os.makedirs(pathname)
            os.chdir(pathname)
            img = satname.wms_req(dates[d])
            with open(satname.abr[0] + dates[d] + '.png', 'wb') as out:
                out.write(img.read())
        os.chdir('..')           
    else:
        pathname = region + '_' + str(date)
        os.makedirs(pathname)
        os.chdir(pathname)
        #create subdirectories for each satellite

if __name__ == "__main__":
    main()