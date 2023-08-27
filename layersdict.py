MODIS_Terra_CorrectedReflectance_TrueColor = {
    "xmin": -20037508.3427892,
    "ymin": -20037508.3427892,
    "xmax": 20037508.3427892,
    "ymax": 20037508.3427892,
    "crs": "EPSG:3857",
    "wms": "https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?",
    "layer": ["MODIS_Terra_CorrectedReflectance_TrueColor"],
    "size": (1200, 600),
    "format": "image/png",
    "transparent": True,
    "Time_format": False

}

#Example of thermal anomalies relevant to wildfires
#Uses wms service and converts vector to png image
#note different projection and bounds

VIIRS_NOAA20_Thermal_Anomalies_375m_All = {
    "xmin": -180,
    "ymin": -90,
    "xmax": 180,
    "ymax": 90,
    "crs": "EPSG:4326",
    "wms": "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?",
    "layer": ["VIIRS_NOAA20_Thermal_Anomalies_375m_All"],
    "size": (1200, 600),
    "format": "image/png",
    "transparent": True,
    "Time_format": True

}

#note, shapefile projection cannot be different than wms projection