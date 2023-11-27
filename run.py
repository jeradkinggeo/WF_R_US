import DataNormTool
from DataNormTool import bbox_calculator as bbox
from DataNormTool import DataNormTool as dn
import WMS_API_Tool.layersclass as lc
import time 


overwrite = True

def main():

    print("Howdy! Welcome to the Wildfires 'R' Us tool.")
    time.sleep(1)
    print("If you need help, type help to provide a list of commands")
    while True:
        command = input(">: ")
        if command.lower() == "exit":
            exit()                    
        elif command.lower() == "help":
            print("""Commands:
            Display list of fires in the CalFire GDB, "list":
            Run the tool, "run":""")
        elif command.lower() == "list": 
            print('List of fires, show_recs:' )
            shpname, shppath = dn.shapefile_finder("FireGDB")
            dn.show_recs(shppath)
        elif command.lower() == "run":
            userinput = input("Enter FIRE NAME: ")
            userinput = str(userinput)

            sfinput = input("Enter the desired scale factor (Recommended 1000): ")
            sfinput = int(sfinput)
            
            shpname, shppath = dn.shapefile_finder("FireGDB")

            attr_req = input("Would you like a txt log of the fire attributes (y/n): ")

            if attr_req.lower() == 'y':
                dn.attributes_to_log(shppath, "fire_attributes.txt", userinput)
            elif attr_req.lower() == 'n':
                pass

            fire_attr_dict, bounds = dn.QueryAndParamPull(shppath, 'FIRE_NAME', userinput)

            datelist = dn.create_date_list(fire_attr_dict['ALARM_DATE'], fire_attr_dict['CONT_DATE'])

            satlist = [lc.VIIRS_NOAA20_Thermal_Anomalies_375m_All, lc.MODIS_Combined_Thermal_Anomalies_All, lc.MODIS_Aqua_Terra_AOD,
                    lc.MODIS_Terra_CorrectedReflectance_TrueColor, lc.VIIRS_NOAA20_LST]
            satlist = lc.layer_check(satlist,datelist)

            for layer in satlist:
                if layer.crs == 'EPSG:4326':
                    layer.xmin, layer.ymin, layer.xmax, layer.ymax = bounds
                elif layer.crs == 'EPSG:3857':
                    coordtransform = lc.coord_transformer(bounds)
                    layer.xmin, layer.ymin, layer.xmax, layer.ymax = coordtransform

            for layer in satlist:
                if layer.crs == 'EPSG:4326':
                    lc.resolution_calc(layer, sfinput)
                elif layer.crs == 'EPSG:3857':
                    lc.resolution_calc(layer, (sfinput/sfinput) * .1)
        
            lc.layer_pull(satlist, datelist, fire_attr_dict['FIRE_NAME'])
        


if __name__ == "__main__":
    main()