from owslib.wms import WebMapService

class layer:
    def __init__(self, xmin, ymin, xmax, ymax, crs, wms, layer_name, abr, size, format, transparent, Time_format):
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

#Define a couple of layers

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

#Define a couple of layers
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



    

