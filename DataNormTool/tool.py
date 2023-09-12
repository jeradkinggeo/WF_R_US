import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os

input_shapefile = "input.shp"
output_shapefile = "output.shp"

def main():
    os.chdir(r"C:\Users\jerad_kpmetvk\Desktop\WFDir\WF_R_US\ArcTools\TestShapes")
    filter_shapefile_fields("input.shp", "output.shp")
    print("Filtering shapefile fields...")
    append_fields_to_shapefile("output.shp",  "output_with_fields.shp", "3-10-2000", "9-12-2002", "Url.com", "Big Fire")
    


def filter_shapefile_fields(input_shapefile, output_shapefile):
    # Open the input shapefile
    with fiona.open(input_shapefile, 'r') as source:

        # Create a schema for the output shapefile
        output_schema = {
            'geometry': source.schema['geometry'],
            'properties': {}
        }

        # If OBJECTID exists in the input shapefile, add it to the output shapefile schema
        if 'OBJECTID' in source.schema['properties']:
            output_schema['properties']['OBJECTID'] = source.schema['properties']['OBJECTID']

        # Write the output shapefile with filtered attributes
        with fiona.open(output_shapefile, 'w',
                        crs=to_string(source.crs),
                        driver=source.driver,
                        schema=output_schema) as dest:

            for feature in source:
                # Copy only the geometry and OBJECTID if it exists
                output_feature = {
                    'geometry': mapping(shape(feature['geometry'])),
                    'properties': {}
                }
                
                if 'OBJECTID' in feature['properties']:
                    output_feature['properties']['OBJECTID'] = feature['properties']['OBJECTID']
                
                dest.write(output_feature)

    print(f"Filtered shapefile saved to {output_shapefile}")


def append_fields_to_shapefile(input_shapefile, output_shapefile, start_date, end_date, fire_name, source_name):
    # Open the input shapefile
    with fiona.open(input_shapefile, 'r') as source_file:
        
        # Create a new schema with only geometry and the new fields
        output_schema = {
            'geometry': source_file.schema['geometry'],
            'properties': {
                'StartDate': 'str:80',
                'EndDate': 'str:80',
                'FireName': 'str:80',
                'SourceName': 'str:80'
            }
        }
        
        # Write the output shapefile with the new fields
        with fiona.open(output_shapefile, 'w',
                        crs=to_string(source_file.crs),
                        driver=source_file.driver,
                        schema=output_schema) as dest:
            
            for feature in source_file:
                # Copy the geometry
                output_feature = {
                    'geometry': mapping(shape(feature['geometry'])),
                    'properties': {}
                }
                
                # Populate new fields with the values passed to the function
                output_feature['properties']['StartDate'] = start_date
                output_feature['properties']['EndDate'] = end_date
                output_feature['properties']['FireName'] = fire_name
                output_feature['properties']['SourceName'] = source_name
                
                dest.write(output_feature)

    print(f"Shapefile with appended fields saved to {output_shapefile}")



if __name__ == "__main__":
    main()
