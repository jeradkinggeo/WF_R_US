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
from layersclass import layer
import time



overwrite = True

def main():
    satlist = [lc.MODIS_Terra_CorrectedReflectance_TrueColor, 
               lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All,
               lc.MODIS_Aqua_Terra_AOD,
               ]
    dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]
    #Note, Imgdir_make includes the WMS Req function.    
    layer_pull(satlist, dates[1::], 'World')
    #print(satlist[0].layer_attr(satlist[0].wms))
    
def layer_pull(satname, date, region):
    sat = satname
    if isinstance(date, list) and isinstance(satname, list):
        dates = date
        pri_dir = "Image_Directory"
        os.chdir("WMS_API_Tool")
        if os.path.exists(pri_dir):        
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
        else:
            os.mkdir(pri_dir)
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
        os.chdir("WMS_API_Tool")
        pri_dir = "Image_Directory"
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