import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os
import DataNormTool as dn

def main():
    [inp, path] = dn.find_shapefile_in_directory("ShapesDir")
    dn.append_fields_to_shapefile(inp, path, "3-10-2000", "9-12-2002", "BigFire", "URL.com")


if __name__ == "__main__":
    main()
