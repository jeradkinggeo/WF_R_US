from owslib.wms import WebMapService

class layer:
    def __init__(self, xmin, ymin, xmax, ymax, crs, wms, layer_name, size, format, transparent, Time_format):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.crs = crs
        self.wms = wms
        self.name = layer_name
        self.size = size
        self.format = format
        self.transparent = transparent
        self.Time_format = Time_format


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


    



    

