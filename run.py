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
import geopandas as gpd



overwrite = True

def main():

    sfinput = input("Enter the desired scale factor (Recommended 1000): ")
    sfinput = int(sfinput)
    # queryinp1 = input("Desired Query Method (OBJECTID or FIRE_NAME): ")
    # queryinp1 = str("Desired Query Method (OBJECTID or FIRE_NAME): ")
    
    userinput = input("Enter OBJECTID or FIRE_NAME: ")
    userinput = str(userinput)

    shpname, shppath = dn.shapefile_finder("FireGDB")
    fire_attr_dict, bounds = dn.QueryAndParamPull(shppath, 'FIRE_NAME', userinput)
    datelist = dn.create_date_list(fire_attr_dict['ALARM_DATE'], fire_attr_dict['CONT_DATE'])
    satlist = [lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All, lc.MODIS_Aqua_Terra_AOD, lc.MODIS_Terra_CorrectedReflectance_TrueColor]

    for layer in satlist:
        if layer.crs == 'EPSG:4326':
            layer.xmin, layer.ymin, layer.xmax, layer.ymax = bounds
        elif layer.crs == 'EPSG:3857':
            coordtransform = lc.coord_transformer(bounds)
            layer.xmin, layer.ymin, layer.xmax, layer.ymax = coordtransform

    
    lc.resolution_calc(lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All, sfinput)
    lc.resolution_calc(lc.MODIS_Aqua_Terra_AOD, sfinput)
    lc.resolution_calc(lc.MODIS_Terra_CorrectedReflectance_TrueColor, (sfinput/sfinput) * .1)
    # current_width , current_height = lc.MODIS_Terra_CorrectedReflectance_TrueColor.size
    # current_width = current_width * .1
    # current_height = current_height * .1
    # lc.MODIS_Terra_CorrectedReflectance_TrueColor.size = (current_width, current_height)

    
    lc.layer_pull(satlist, datelist, fire_attr_dict['FIRE_NAME'])
    


if __name__ == "__main__":
    main()