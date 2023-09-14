import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os
import DataNormTool as dn

def main():
    [inp, path] = dn.shapefile_finder("ShapesDir")
    # startdate = input("Enter start date (year-month-day): ")
    # enddate = input("Enter end date (year-month-day): ")
    # firename = input("Enter fire name: ")
    # sourcename = input("Enter source name: ")
    dn.shapefile_normalization(inp, path, "3-10-2000", "9-12-2002", "BigFire", "URL.com")


if __name__ == "__main__":
    main()
