from owslib.wms import WebMapService
import requests
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree

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
    
    def layer_attr(self):
        wmsURL = self.wms
        wmsUrl = wmsURL + 'service=WMS&version=1.1.1&request=GetCapabilities'
        response = requests.get(wmsUrl)
        WmsTree = xmltree.fromstring(response.content)
        layerName = self.name
        for child in WmsTree.iter():
            if child.tag == '{http://www.opengis.net/wms}WMS_Capabilities': 
                print('Version: ' +child.get('version'))
            
            if child.tag == '{http://www.opengis.net/wms}Service': 
                print('Service: ' +child.find("{http://www.opengis.net/wms}Name").text)
                
            if child.tag == '{http://www.opengis.net/wms}Request': 
                print('Request: ')
                for e in child:
                    print('\t ' + e.tag.partition('}')[2])
                                    
                all = child.findall(".//{http://www.opengis.net/wms}Format")
                if all is not None:
                    print("Format: ")
                    for g in all:
                        print("\t " + g.text)     
                        
                for e in child.iter():
                    if e.tag == "{http://www.opengis.net/wms}OnlineResource":
                        print('URL: ' + e.get('{http://www.w3.org/1999/xlink}href'))
                        break

                for child in WmsTree.iter():
                    for layer in child.findall("./{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer//*/"): 
                        if layer.tag == '{http://www.opengis.net/wms}Layer': 
                            f = layer.find("{http://www.opengis.net/wms}Name")
                            if f is not None:
                                if f.text == layerName:
                                    # Layer name.
                                    print('Layer: ' + f.text)
                                    
                                    # All elements and attributes:
                                    # CRS
                                    e = layer.find("{http://www.opengis.net/wms}CRS")
                                    if e is not None:
                                        print('\t CRS: ' + e.text)
                                    
                                    # BoundingBox.
                                    e = layer.find("{http://www.opengis.net/wms}EX_GeographicBoundingBox")
                                    if e is not None:
                                        print('\t LonMin: ' + e.find("{http://www.opengis.net/wms}westBoundLongitude").text)
                                        print('\t LonMax: ' + e.find("{http://www.opengis.net/wms}eastBoundLongitude").text)
                                        print('\t LatMin: ' + e.find("{http://www.opengis.net/wms}southBoundLatitude").text)
                                        print('\t LatMax: ' + e.find("{http://www.opengis.net/wms}northBoundLatitude").text)
                                    
                                    # Time extent.
                                    e = layer.find("{http://www.opengis.net/wms}Dimension")
                                    if e is not None:
                                        print('\t TimeExtent: ' + e.text)
                                        
                                    # Style.
                                    e = layer.find("{http://www.opengis.net/wms}Style")
                                    if e is not None:
                                        f = e.find("{http://www.opengis.net/wms}Name")
                                        if f is not None:
                                            print('\t Style: ' + f.text)


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