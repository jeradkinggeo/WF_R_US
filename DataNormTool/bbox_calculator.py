import fiona
from fiona.crs import to_string
import shapely
from shapely.geometry import shape, mapping, Polygon
import os
import time
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    shpname, shpfp =  shapefile_finder("ShapesDir")
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

def shapefile_finder(DataDir):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full path to your DataDir
    full_path = os.path.join(current_directory, "DataNormTool", DataDir)

    print("Searching in:", full_path)

    try:
        all_files = os.listdir(full_path)
    except FileNotFoundError:
        print(f"Directory {full_path} not found.")
        return None, None

    # Filter out the files that have a .shp extension
    shapefiles = [f for f in all_files if f.endswith('.shp')]

    # If shapefiles are found, return the first one along with its full path
    if shapefiles:
        shapefile_name = shapefiles[0]
        return shapefile_name, full_path
    else:
        return None, None
    
if __name__ == '__main__':
    main()