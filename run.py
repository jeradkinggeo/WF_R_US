import os
from io import BytesIO
from skimage import io
import inspect
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
import DataNormTool
from DataNormTool import bbox_calculator as bbox
from DataNormTool import DataNormTool as dn
import WMS_API_Tool.layersclass as lc
import time



overwrite = True

def main():
    # satlist = [lc.MODIS_Terra_CorrectedReflectance_TrueColor, 
    #            lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All,
    #            lc.MODIS_Aqua_Terra_AOD,
    #            ]
    dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]
    [inp, path] = dn.shapefile_finder("ShapesDir")
    out = bbox.shp_extent(path)
    print(out)
    satlist = [lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All, lc.MODIS_Aqua_Terra_AOD]
    for layer in satlist:
        layer.xmin, layer.ymin, layer.xmax, layer.ymax = out

    lc.resolution_calc(lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All)
    lc.resolution_calc(lc.MODIS_Aqua_Terra_AOD)
    lc.layer_pull(satlist, dates[1:], 'California')
    # #Note, Imgdir_make includes the WMS Req function.    
    # lc.layer_pull(satlist, dates[1::], 'World')
    # #print(satlist[0].layer_attr(satlist[0].wms))
    


if __name__ == "__main__":
    main()