import pprint, numpy as np, rasterio, rasterio.features, fiona, matplotlib.pyplot as plt, json
from affine import Affine
from scipy.stats.mstats import mquantiles
from shapely.geometry import shape
from tqdm import *

pp = pprint.PrettyPrinter(indent=2)

def clip_and_pull(vname, rname, dump=False):
    county = {}
    with fiona.open(vname, 'r') as vector, rasterio.open(rname, 'r') as raster:
        for feature in tqdm(vector):
            # create a shapely geometry
            # this is done for the convenience for the .bounds property only
            geometry = shape(feature['geometry'])
            cntyid = feature['properties'][u'GEOID']
            county[cntyid] = {}

            # get pixel coordinates of the geometry's bounding box
            ul = raster.index(*geometry.bounds[0:2])
            lr = raster.index(*geometry.bounds[2:4])

            # read the subset of the data into a numpy array
            window = ((lr[0], ul[0]+1), (ul[1], lr[1]+1))
            data = raster.read(1, window=window)

            # create an affine transform for the subset data
            t = raster.affine
            shifted_affine = Affine(t.a, t.b, t.c+ul[1]*t.a, t.d, t.e, t.f+lr[0]*t.e)

            # rasterize the geometry
            mask = rasterio.features.rasterize(
                [(geometry, 0)],
                out_shape=data.shape,
                transform=shifted_affine,
                fill=1,
                all_touched=True,
                dtype=np.uint8)

            # create a masked numpy array
            masked_data = np.ma.array(data=data, mask=mask.astype(bool))

            # calculate statistics at county level
            county[cntyid]['sum'] = float(np.ma.sum(masked_data))
            county[cntyid]['mean'] = float(np.ma.mean(masked_data))
            county[cntyid]['std'] = float(np.ma.std(masked_data))
            county[cntyid]['quantiles'] = [ float(x) for x in mquantiles(masked_data, prob=[0,0.05,.1, .2, 0.3,0.4,.5, 0.6,0.7, 0.8, 0.9,0.95, 1], alphap=1, betap=1).tolist() ]

    # save a copy
    if dump:
        with open('%s.json'%rname, 'wb') as f:
            json.dump(county, f)

    return county

if __name__ == '__main__':
    # 201402
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20140201-20140228_75N180W_vcmcfg_v10_c201507201052/SVDNB_npp_20140201-20140228_75N180W_vcmcfg_v10_c201507201052.avg_rade9.tif', dump=True)
    # 201404
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20140401-20140430_75N180W_vcmcfg_v10_c201507201613/SVDNB_npp_20140401-20140430_75N180W_vcmcfg_v10_c201507201613.avg_rade9.tif', dump=True)
    # 201406
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20140601-20140630_75N180W_vcmcfg_v10_c201502121156/SVDNB_npp_20140601-20140630_75N180W_vcmcfg_v10_c201502121156.avg_rade9.tif', dump=True)
    # 201408
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20140801-20140831_75N180W_vcmcfg_v10_c201508131459/SVDNB_npp_20140801-20140831_75N180W_vcmcfg_v10_c201508131459.avg_rade9.tif', dump=True)
    # 201410
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20141001-20141031_75N180W_vcmcfg_v10_c201502231115/SVDNB_npp_20141001-20141031_75N180W_vcmcfg_v10_c201502231115.avg_rade9.tif', dump=True)
    # 201412
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20141201-20141231_75N180W_vcmcfg_v10_c201502231125/SVDNB_npp_20141201-20141231_75N180W_vcmcfg_v10_c201502231125.avg_rade9.tif', dump=True)
    # 201502
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20150201-20150228_75N180W_vcmcfg_v10_c201504281504/SVDNB_npp_20150201-20150228_75N180W_vcmcfg_v10_c201504281504.avg_rade9.tif', dump=True)
    # 201504
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20150401-20150430_75N180W_vcmcfg_v10_c201506011707/SVDNB_npp_20150401-20150430_75N180W_vcmcfg_v10_c201506011707.avg_rade9.tif', dump=True)
    # 201506
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20150601-20150630_75N180W_vcmcfg_v10_c201508141522/SVDNB_npp_20150601-20150630_75N180W_vcmcfg_v10_c201508141522.avg_rade9.tif', dump=True)
    # 201508
    clip_and_pull('./cb_2014_us_county_20m/cb_2014_us_county_20m.shp', './SVDNB_npp_20150801-20150831_75N180W_vcmcfg_v10_c201509301759/SVDNB_npp_20150801-20150831_75N180W_vcmcfg_v10_c201509301759.avg_rade9.tif', dump=True)
