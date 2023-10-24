import fiona
from fiona.crs import to_string
import shapely
from shapely.geometry import shape, mapping, Polygon
import os
import time
import geopandas as gpd
import matplotlib.pyplot as plt
import DataNormTool as dn
import time

#Modify this file such that there is only one function that needs to be 
#Run to calculate the bounding box of a shapefile.

def main():
    shpname, shpfp =  dn.shapefile_finder("ShapesDir")
    shapefile_path = shpfp
    gdf = gpd.read_file(shapefile_path)
    centroids = poly_centroid(shapefile_path)
    extent = poly_extent(gdf)
    #conlist = bboxpass(extent)
    time.sleep(2)
    #print(conlist)

    # Plotting
    fig, ax = plt.subplots()
    gdf.boundary.plot(ax=ax, color='blue', linewidth=1)
    centroids.plot(ax=ax, color='red', marker='o', markersize=5, label='Centroids')

    # Draw bounding boxes around each centroid
    for centroid in centroids:
        rect = plt.Rectangle((extent[0], extent[1]), 
                            extent[2]-extent[0], 
                            extent[3]-extent[1], 
                            linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    ax.set_title('Bounding Box around Centroid')
    plt.legend()
    plt.show()


def poly_centroid(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    centroids = gdf.geometry.centroid
    return centroids

def poly_extent(gdf):
    bounds = gdf.total_bounds
    return (bounds[0], bounds[1], bounds[2], bounds[3])
    

import geopandas as gpd

def compute_extents_from_shapefile(shapefile_path):
    def compute_shapefile_centroid(gdf):
        return gdf.geometry.centroid
    
    def shapefile_extent(gdf):
        bounds = gdf.total_bounds
        return (bounds[0], bounds[1], bounds[2], bounds[3])

    def bounding_box_corners(centroid, extent):
        corners = [
            (extent[0], extent[1]),
            (extent[0], extent[3]),
            (extent[2], extent[1]),
            (extent[2], extent[3])
        ]
        return corners
    
    def corner_pull(corners):
        x_values = [corner[0] for corner in corners]
        y_values = [corner[1] for corner in corners]
        return (min(x_values), min(y_values), max(x_values), max(y_values))

    # Main function body
    gdf = gpd.read_file(shapefile_path)
    centroids = compute_shapefile_centroid(gdf)
    extent = shapefile_extent(gdf)

    corners_list = [bounding_box_corners(centroid, extent) for centroid in centroids]
    extents_list = [corner_pull(corners) for corners in corners_list]

    return extents_list

if __name__ == '__main__':
    main()