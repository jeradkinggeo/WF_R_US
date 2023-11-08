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
    shpname, shppath = dn.shapefile_finder("FireGDB")
    fire_attr_dict, bounds = dn.QueryAndParamPull(shppath, 'FIRE_NAME', 'SILVERADO')
    datelist = dn.create_date_list(fire_attr_dict['ALARM_DATE'], fire_attr_dict['CONT_DATE'])
    print(datelist)
    satlist = [lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All, lc.MODIS_Aqua_Terra_AOD]
    # dates = ["2019-09-12","2020-09-12","2021-09-12","2022-09-12"]
    # [inp, path] = dn.shapefile_finder("ShapesDir")
    # out = bbox.shp_extent(path)
    # print(out)
    # satlist = [lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All, lc.MODIS_Aqua_Terra_AOD]
    for layer in satlist:
        layer.xmin, layer.ymin, layer.xmax, layer.ymax = bounds

    lc.resolution_calc(lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All)
    lc.resolution_calc(lc.MODIS_Aqua_Terra_AOD)
    
    lc.layer_pull(satlist, datelist, fire_attr_dict['FIRE_NAME'])
    


if __name__ == "__main__":
    main()