import fiona
from fiona.crs import to_string
import shapely
from shapely.geometry import shape, mapping, Polygon
import os
import time
import geopandas as gpd
import matplotlib.pyplot as plt
os.path.join(os.getcwd(), "DataNormTool")
import DataNormTool as dn

def main():
    shpname, shpfp =  dn.shapefile_finder("ShapesDir")
    shapefile_path = shpfp
    gdf = gpd.read_file(shapefile_path)
    centroids = shp_centroid(shapefile_path)
    extent = shp_extent(shapefile_path)
    print(extent)

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

    ax.set_title('Bounding Box around Each Centroid')
    plt.legend()
    plt.show()


def shp_centroid(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    centroids = gdf.geometry.centroid
    return centroids

def shp_extent(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    bounds = gdf.total_bounds
    return (bounds[0], bounds[1], bounds[2], bounds[3])


if __name__ == '__main__':
    main()