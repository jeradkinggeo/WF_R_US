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

os.path.join()

overwrite = True

def main():
    # satlist = [lc.MODIS_Terra_CorrectedReflectance_TrueColor, 
    #            lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All,
    #            lc.MODIS_Aqua_Terra_AOD,
    #            ]
    import bbox_calculator as bbox
    satlist = [lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All]
    dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]
    bounds = [-124.41501099999999, 32.534374263000075, 
              -114.13122247499996, 42.009508270000026]
    lc.set_bbox(bounds)
    lc.resolution_calc()
    # #Note, Imgdir_make includes the WMS Req function.    
    # lc.layer_pull(satlist, dates[1::], 'World')
    # #print(satlist[0].layer_attr(satlist[0].wms))
    


if __name__ == "__main__":
    main()