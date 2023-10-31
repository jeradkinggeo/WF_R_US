Description of functions contained within each directory and module


-----WMS_API_Tool-----
The WMS API Tool directory contains modules responsible for communicating with the GIBS API and defines the layer class objects.

run.py: This is the program used for actually retrieving the layers from the GIBS API. Only consists of a main function and imports from the layerclass module. 

When run, an image directory will be created within the cwd 

-Pending changes- 
File is currently hardcoded to dates, this will be iteratively passed to the layer_pull function from the database.

layerclass.py: The function of this module is to create the class layer. The relevant attributes for calling the layer from the GIBS api are defined as attributes of the class. 

-wms_resp(self, wms)- Pulls the XML tree for WMS (Web Mapping Service)
-wms_req(self, timeP)- Requests the layer from the webmapping service
-layer_pull(satname, date, region)- Downloads the layer(s) according to the requested layer (satname), the date(s), and the region. 

-Pending changes- 
The region is currently hardcoded within the actual class object for each layer, with the region currently defined as the world (-180, -90, etc)


-----DataNormTool-----
This directory contains the modules responsible for parsing information from shapefiles and turning them into a format that has utility for the GIBS API requests.

bbox_calculator.py: This is an important module that parses the geometric information from the shapefile.

-main- Has a plotting function that takes multiple functions within the bbox_calc function and spits out a graph of the bounding box around the shapefile geometry.
-shp_centroid(shapefile_path)- Finds centroid of shapefile, returns centroid.
-shp_extent(gdf)- Takes arg gdf (called via gdf = gpd.read_file(shapefile_path)) and returns bounds. 
 



