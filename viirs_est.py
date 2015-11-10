import tqdm, pprint, numpy as np

from PIL import Image

pp = pprint.PrettyPrinter(indent=2)

im = Image.open('./SVDNB_npp_20140201-20140228_75N180W_vcmcfg_v10_c201507201052/SVDNB_npp_20140201-20140228_75N180W_vcmcfg_v10_c201507201052.avg_rade9.tif')

np_im = np.array(im)
pp.pprint(np_im.shape)