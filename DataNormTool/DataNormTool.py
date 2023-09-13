import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os
import time

def find_shapefile_in_directory(DataDir):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full path to your DataDir
    full_path = os.path.join(current_directory, "DataNormTool", DataDir)

    print("Searching in:", full_path)

    try:
        all_files = os.listdir(full_path)
    except FileNotFoundError:
        print(f"Directory {full_path} not found.")
        return None, None

    # Filter out the files that have a .shp extension
    shapefiles = [f for f in all_files if f.endswith('.shp')]

    # If shapefiles are found, return the first one along with its full path
    if shapefiles:
        shapefile_name = shapefiles[0]
        return shapefile_name, full_path
    else:
        return None, None

def append_fields_to_shapefile(input_shapefile, ShpDir, start_date, end_date, fire_name, source_name):
    # Change working directory to ShpDir
    os.chdir(ShpDir)

    # Create a new directory with fire_name and start_date
    output_directory = f"{fire_name}_{start_date}"
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    
    # Define the path for the output shapefile inside the new directory
    output_shapefile_path = os.path.join(output_directory, "output_shapefile.shp")

    # Open the input shapefile
    with fiona.open(input_shapefile, 'r') as source:
        # Create a schema for the output shapefile, only keeping geometry and new fields
        output_schema = {
            'geometry': source.schema['geometry'],
            'properties': {
                'StartDate': 'str:80',
                'EndDate': 'str:80',
                'FireName': 'str:80',
                'SourceName': 'str:80'
            }
        }
        
        # If OBJECTID exists, add it to the output schema
        if 'OBJECTID' in source.schema['properties']:
            output_schema['properties']['OBJECTID'] = source.schema['properties']['OBJECTID']
        
        # Write the output shapefile
        with fiona.open(output_shapefile_path, 'w',
                        crs=to_string(source.crs),
                        driver=source.driver,
                        schema=output_schema) as dest:
            
            for feature in source:
                # Initialize output feature with only the geometry
                output_feature = {
                    'geometry': mapping(shape(feature['geometry'])),
                    'properties': {}
                }

                # Copy OBJECTID if it exists
                if 'OBJECTID' in feature['properties']:
                    output_feature['properties']['OBJECTID'] = feature['properties']['OBJECTID']
                
                # Populate new fields
                output_feature['properties']['StartDate'] = start_date
                output_feature['properties']['EndDate'] = end_date
                output_feature['properties']['FireName'] = fire_name
                output_feature['properties']['SourceName'] = source_name
                
                dest.write(output_feature)
        
    print(f"Shapefile with appended fields saved to {output_shapefile_path}")
