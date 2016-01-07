## Processing VIIRS Raster Files to County through Python
###### Using Rasterio, Shapely, and Fiona

##> Summary
1. Convert the raster into a numpy array
2. Draw a box that contains the county polygon
3. Clip the array to the box
4. Define affine transform on shapefile to raster
4. Create array mask of shape of county in box using Rasterio
5. Calculate necessary measures on masked array
