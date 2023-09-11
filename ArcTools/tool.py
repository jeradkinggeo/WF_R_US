import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os

os.chdir(r"C:\Users\jerad_kpmetvk\Desktop\WFDir\WF_R_US\ArcTools\Test Shapes")

input_shapefile = "input.shp"
output_shapefile = "output.shp"

def main():
    print("Filtering shapefile fields...")


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


def append_fields_to_shapefile(input_shapefile, output_shapefile):
    # Open the input shapefile
    with fiona.open(input_shapefile, 'r') as source:

        # Copy the existing schema and add new fields
        output_schema = source.schema.copy()
        output_schema['properties']['Start_Date'] = 'str:80'  # String field with max length of 80
        output_schema['properties']['End_Date'] = 'float'   # Float field
        output_schema['properties']['Source'] = 'int'     # Integer field
        output_schema['properties']['Fire Name'] = 'str:80'  # Another string field with max length of 80

        # Write the output shapefile with the new fields
        with fiona.open(output_shapefile, 'w',
                        crs=to_string(source.crs),
                        driver=source.driver,
                        schema=output_schema) as dest:

            for feature in source:
                # Copy existing feature attributes and geometry
                output_feature = {
                    'geometry': mapping(shape(feature['geometry'])),
                    'properties': feature['properties'].copy()
                }

                # Populate new fields with default values (you can adjust these)
                output_feature['properties']['Field1'] = "default_value1"
                output_feature['properties']['Field2'] = 0.0
                output_feature['properties']['Field3'] = 0
                output_feature['properties']['Field4'] = "default_value4"

                dest.write(output_feature)

    print(f"Shapefile with appended fields saved to {output_shapefile}")

# Example usage
append_fields_to_shapefile("input.shp", "output_with_fields.shp")




if __name__ == "__main__":
    main()
