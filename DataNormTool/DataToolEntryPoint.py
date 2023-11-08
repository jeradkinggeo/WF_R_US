import fiona
from fiona.crs import to_string
from shapely.geometry import shape, mapping
import os
import geopandas as gpd
import DataNormTool as dn

def main():
    print('DataNormTool Test')
    shpname, shppath = dn.shapefile_finder("FireGDB")
    os.chdir('DataNormTool')
    os.chdir('FireGDB')
    gdf = gpd.read_file('FireGDB.shp')
    userinput = input("Enter OBJECTID or FIRE_NAME: ")
    userinput = str(userinput)
    fire_attr_dict, bounds = dn.QueryAndParamPull(shppath, 'FIRE_NAME', userinput)
    print("Fire Name Query", fire_attr_dict)
    print("Bounds", bounds)
    datelist = dn.create_date_list(fire_attr_dict['ALARM_DATE'], fire_attr_dict['CONT_DATE'])
    print(datelist)


if __name__ == "__main__":
    main()
