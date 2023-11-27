from owslib.wms import WebMapService
import requests
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
import os
from pyproj import transform, Proj
import datetime

class layer:
    def __init__(self, crs, wms, layer_name, abr, 
                 size, format, transparent, Time_format):
        self.xmin, self.ymin, self.xmax, self.ymax = None, None, None, None
        self.crs = crs
        self.wms = wms
        self.name = layer_name
        self.abr = abr
        self.size = size
        self.format = format
        self.transparent = transparent
        self.Time_format = Time_format

    def wms_resp(self, wms):
            wmsUrl = wms
            response = requests.get(wmsUrl)
            WmsXml = xmltree.fromstring(response.content)
            result = print(xmltree.tostring(WmsXml, pretty_print = True, encoding = str))
            return result

    def wms_req(self, timeP):
        if self.Time_format == True:
            timeP = timeP + "T00:00:00Z"
        wms = WebMapService(self.wms)
        result = wms.getmap(layers=self.name,  # Layers
                    srs=self.crs,  # Map projection
                    bbox=(self.xmin,self.ymin, self.xmax,self.ymax),  # Bounds
                    size=self.size,  # Image size
                    time=timeP,  # Time of data
                    format=self.format,  # Image format
                    transparent=self.transparent)
        return result
    
def coord_transformer(bounds):
    proj_4326 = Proj(init = 'epsg:4326')
    proj_3857 = Proj(init = 'epsg:3857')
    xmin, ymin = transform(proj_4326, proj_3857, bounds[0], bounds[1])
    xmax, ymax = transform(proj_4326, proj_3857, bounds[2], bounds[3])
    return (xmin, ymin, xmax, ymax)

def layer_pull(satname, date, region):
    sat = satname
    if isinstance(date, list) and isinstance(satname, list):
        dates = date
        pri_dir = "Image_Directory"
        if os.path.exists(pri_dir):        
            os.chdir(pri_dir)
            current_time = datetime.datetime.now().strftime("%m-%d_%H-%M")
            os.mkdir("runtime" + '_' + current_time)
            os.chdir("runtime" + '_' + current_time)
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


MODIS_Terra_CorrectedReflectance_TrueColor = layer(
                                                   'EPSG:3857', 
                                                   'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                                                   ['MODIS_Terra_CorrectedReflectance_TrueColor'],
                                                   'MODIS_TCR', 
                                                   (1200, 600), 
                                                   'image/png', 
                                                   True, 
                                                   False)

VIIRS_NOAA20_Thermal_Anomalies_375m_All = layer(
                                                'EPSG:4326', 
                                                'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                                                ['VIIRS_NOAA20_Thermal_Anomalies_375m_All'],
                                                'VIIRS_TA', 
                                                (1200, 600), 
                                                'image/png', 
                                                True, 
                                                False)

# ^ Only has data past 2020-01-01

VIIRS_NOAA20_LST = layer(
                        'EPSG:4326', 
                        'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                        ['VIIRS_NOAA20_Land_Surface_Temp_Day'],
                        'VIIRS_LST', 
                        (1200, 600), 
                        'image/png', 
                        True, 
                        False)

MODIS_Aqua_Terra_AOD = layer(
                           'EPSG:4326', 
                           'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                            ['MODIS_Combined_MAIAC_L2G_AerosolOpticalDepth'],
                            'MODIS_Terra_AOD', 
                             (1200, 600), 
                             'image/png', 
                              True, 
                              False)

MODIS_Combined_Thermal_Anomalies_All = layer(
                           'EPSG:4326', 
                           'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                            ['MODIS_Combined_Thermal_Anomalies_All'],
                            'MODIS_Terra_TA', 
                             (1200, 600), 
                             'image/png', 
                              True, 
                              True)




def set_bbox(self, bounds):
    self.xmin = bounds[0]
    self.ymin = bounds[1]
    self.xmax = bounds[2]
    self.ymax = bounds[3]
    return self.xmin, self.ymin, self.xmax, self.ymax

def resolution_calc(self, scale):
    scalefactor = scale  
    width = ((self.xmax - self.xmin) * scalefactor)
    height = ((self.ymax - self.ymin) * scalefactor)
    self.size = (width, height)


#Index for layers are hardcoded, but works for now
def layer_check(layerlist, datelist):
    if datelist[0] < '2020-01-01':
        print("VIIRS_NOAA20_Thermal_Anomalies_375m_All does not have data before 2020-01-01")
        return layerlist[1::]
    else:
        layerlist.remove(layerlist[1])
        return layerlist



        

            