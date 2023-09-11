import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os

os.chdir(r"C:\Users\jerad_kpmetvk\Desktop\WFDir\WF_R_US\ArcTools\Test Shapes")

input_shapefile = "input.shp"
output_shapefile = "output.shp"

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