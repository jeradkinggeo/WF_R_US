# Wildfires 'R' Us Imagery Acquisition Tool

### I am no longer actively working on this project. If this interests you, feel free to reach out, submit a PR, etc.

## Description 
This tool is designed to streamline the process of acquiring satellite imagery for wildfire research in California. By leveraging the capabilities of the GIBS API, it allows users to query a comprehensive database of California wildfires and dynamically generates API requests based on specific geodatabase attributes. The result is a collection of image layers highly relevant to wildfire studies and response planning.

## Soon to be added 
-Run script that automatically checks for updates 

-Option for writing images to a directory sorted by layer, rather than date

## Current Features
Dynamic API Requests: Automatically generates GIBS API requests tailored to the selected wildfire attributes.
Highly Relevant Imagery: Retrieves satellite imagery layers focused on aspects critical to wildfire research, such as burn area, smoke dispersion, and vegetation health.

## Dependencies 
owslib.wms
requests
pyproj
datetime
geopandas
matplotlib

## Data Sources
NASA Global Imagery Browser Service
https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/

CalFire 2022 Historical Wildfire Perimeters Geodatabase
https://hub-calfire-forestry.hub.arcgis.com/search
