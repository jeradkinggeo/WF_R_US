from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os
from datetime import datetime, timedelta
import geopandas as gpd
from pyproj import Transformer

def create_date_list(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end - start).days
    date_list = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days + 1)]
    return date_list

def QueryAndParamPull(shapefile_path, query_type, query_value):
    gdf = gpd.read_file(shapefile_path)
    if query_type.lower() == 'objectid':
        queried_gdf = gdf[gdf['OBJECTID'] == query_value]
    elif query_type.lower() == 'fire_name':
        queried_gdf = gdf[gdf['FIRE_NAME'].str.upper() ==query_value.upper()]
    else:
        raise ValueError("Filter type must be 'OBJECTID' or 'FIRE_NAME'")
    
    bounds = queried_gdf.total_bounds

    if not queried_gdf.empty:
        attributes = queried_gdf.iloc[0][['FIRE_NAME', 'ALARM_DATE', 'CONT_DATE']].to_dict()
        return attributes, (bounds[0], bounds[1], bounds[2], bounds[3])
    else:
        print("Oops! No fires were found with this query :(")
        return None

def attributes_to_log(shppath, text_path, query_value):
    gdf = gpd.read_file(shppath)
    queried_gdf = gdf[gdf['FIRE_NAME'].str.upper() == query_value.upper()]
    queried_gdf = queried_gdf.drop(columns=['geometry'])
    with open(text_path, 'w') as file:
        for index, row in queried_gdf.iterrows():
            for attribute, value in row.items():
                file.write(f"{attribute}: {value}\n")
            file.write("\n")  

def shapefile_finder(DataDir):
    current_directory = os.getcwd()

    full_path = os.path.join(current_directory, "DataNormTool", DataDir)

    print("Searching in:", full_path)

    try:
        all_files = os.listdir(full_path)
    except FileNotFoundError:
        print(f"Directory {full_path} not found.")
        return None, None

    shapefiles = [f for f in all_files if f.endswith('.shp')]

    if shapefiles:
        shapefile_name = shapefiles[0]
        return shapefile_name, full_path
    else:
        return None, None
