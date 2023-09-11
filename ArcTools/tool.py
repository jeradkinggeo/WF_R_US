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
    append_fields_to_shapefile("output.shp", "3-10-2000", "9-12-2002", "Url.com", "Big Fire", "output_with_fields.shp")
    


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


def append_fields_to_shapefile(input_shapefile, Start_Date, End_Date, Source, Fire_Name, output_shapefile):
    # Open the input shapefile
    with fiona.open(input_shapefile, 'r') as source:

        # Write the output shapefile with the new fields
        with fiona.open(output_shapefile, 'w',
                        crs=to_string(source.crs),
                        driver=source.driver,) as dest:

            for feature in source:
                # Copy existing feature attributes and geometry
                output_feature = {
                    'geometry': mapping(shape(feature['geometry'])),
                    'properties': feature['properties'].copy()
                }

                # Populate new fields with default values (you can adjust these)
                output_feature['properties']['Start_Date'] = Start_Date
                output_feature['properties']['End_date']  = End_Date
                output_feature['properties']['Source'] = Source
                output_feature['properties']['Fire Name'] = Fire_Name   

                dest.write(output_feature)

    print(f"Shapefile with appended fields saved to {output_shapefile}")


if __name__ == "__main__":
    main()
