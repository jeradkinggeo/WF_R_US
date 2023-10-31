from owslib.wms import WebMapService
import requests
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
import os

class layer:
    def __init__(self, xmin, ymin, xmax, ymax, crs, wms, layer_name, abr, 
                 size, format, transparent, Time_format):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
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

#Defining layers
MODIS_Terra_CorrectedReflectance_TrueColor = layer(-20037508.3427892, 
                                                   -20037508.3427892, 
                                                   20037508.3427892, 
                                                   20037508.3427892, 
                                                   'EPSG:3857', 
                                                   'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                                                   ['MODIS_Terra_CorrectedReflectance_TrueColor'],
                                                   'MODIS_TCR', 
                                                   (1200, 600), 
                                                   'image/png', 
                                                   True, 
                                                   False)

VIIRS_NOAA20_Thermal_Anomalies_375m_All = layer(-180, 
                                                -90, 
                                                180, 
                                                90, 
                                                'EPSG:4326', 
                                                'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                                                ['VIIRS_NOAA20_Thermal_Anomalies_375m_All'],
                                                'VIIRS_TA', 
                                                (1200, 600), 
                                                'image/png', 
                                                True, 
                                                True)

MODIS_Aqua_Terra_AOD = layer(-180, 
                         -90, 
                           180, 
                           90, 
                           'EPSG:4326', 
                           'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', 
                            ['MODIS_Combined_MAIAC_L2G_AerosolOpticalDepth'],
                            'MODIS_Terra_AOD', 
                             (1200, 600), 
                             'image/png', 
                              True, 
                              True)