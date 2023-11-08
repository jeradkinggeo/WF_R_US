import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os
import time
from datetime import datetime, timedelta
import geopandas as gpd

def create_date_list(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end - start).days
    date_list = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days + 1)]
    return date_list

def QueryAndParamPull(shapefile_path, filter_type, filter_value):
    gdf = gpd.read_file(shapefile_path)
    # Filter the GeoDataFrame based on the input filter_type and filter_value
    if filter_type.lower() == 'objectid':
        filtered_gdf = gdf[gdf['OBJECTID'] == filter_value]
    elif filter_type.lower() == 'fire_name':
        filtered_gdf = gdf[gdf['FIRE_NAME'].str.upper() == filter_value.upper()]
    else:
        raise ValueError("Filter type must be 'OBJECTID' or 'FIRE_NAME'")
    
    bounds = gdf.total_bounds

    # If the filter results in at least one row, extract the attributes
    if not filtered_gdf.empty:
        attributes = filtered_gdf.iloc[0][['FIRE_NAME', 'ALARM_DATE', 'CONT_DATE']].to_dict()
        return attributes, (bounds[0], bounds[1], bounds[2], bounds[3])
    else:
        return None


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
