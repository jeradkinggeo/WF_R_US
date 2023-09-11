#Nore, interp path must be changed to your arcpy path :/


import arcpy
import os

def multipart_to_singlepart(in_feature_class, out_feature_class, start_date, end_date, input3, input4):
    # Local variables
    temp_singlepart = "temp_singlepart"

    try:
        # Process: Multipart To Singlepart
        arcpy.MultipartToSinglepart_management(in_feature_class, temp_singlepart)

        # Process: Add/Update Fields and Attributes
        fields = arcpy.ListFields(temp_singlepart)
        field_names = [field.name for field in fields]
        
        # Check if 'StartDate', 'EndDate', 'Input3', and 'Input4' exist, if not, create them
        if 'StartDate' not in field_names:
            arcpy.AddField_management(temp_singlepart, 'StartDate', 'DATE')
        if 'EndDate' not in field_names:
            arcpy.AddField_management(temp_singlepart, 'EndDate', 'DATE')
        if 'Input3' not in field_names:
            arcpy.AddField_management(temp_singlepart, 'Input3', 'TEXT')
        if 'Input4' not in field_names:
            arcpy.AddField_management(temp_singlepart, 'Input4', 'TEXT')

        # Update attributes
        with arcpy.da.UpdateCursor(temp_singlepart, ['StartDate', 'EndDate', 'Input3', 'Input4']) as cursor:
            for row in cursor:
                row[0] = start_date
                row[1] = end_date
                row[2] = input3
                row[3] = input4
                cursor.updateRow(row)

        # Process: Create the output feature class
        arcpy.CopyFeatures_management(temp_singlepart, out_feature_class)
        
        arcpy.AddMessage("Successfully converted multipart polygons to singlepart polygons and updated attributes.")

    except Exception as e:
        arcpy.AddError(str(e))

if __name__ == '__main__':
    # Define input parameters
    in_feature_class = arcpy.GetParameterAsText(0)  # Input Feature Class
    out_feature_class = arcpy.GetParameterAsText(1)  # Output Feature Class
    start_date = arcpy.GetParameterAsText(2)  # Start Date
    end_date = arcpy.GetParameterAsText(3)  # End Date
    input3 = arcpy.GetParameterAsText(4)  # Input 3
    input4 = arcpy.GetParameterAsText(5)  # Input 4
    
    multipart_to_singlepart(in_feature_class, out_feature_class, start_date, end_date, input3, input4)
