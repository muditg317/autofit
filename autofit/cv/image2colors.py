from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It contains helper methods for extracting color information from images.")

import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
# from skimage.color import rgb2lab, deltaE_cie76
import os
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
from typing import List

def get_foreground_mask(img, grabcut_iterations=10):
  mask = np.zeros(img.shape[:2],np.uint8)   # img.shape[:2] = (413, 620)

  bgdModel = np.zeros((1,65),np.float64)
  fgdModel = np.zeros((1,65),np.float64)

  rect = (0,0,img.shape[1]-1,img.shape[0]-1)

  print(f'Starting masking process with bounding box: {rect}')
  # this modifies mask 
  cv2.grabCut(img,mask,rect,bgdModel,fgdModel,1,cv2.GC_INIT_WITH_RECT)
  for i in range(grabcut_iterations-1):
    # print('did one grabcut iteration')
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,1,cv2.GC_INIT_WITH_MASK)
  print(f'done with {grabcut_iterations} grabcut iterations')

  # If mask==2 or mask== 1, mask2 get 0, other wise it gets 1 as 'uint8' type.
  mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

  # adding additional dimension for rgb to the mask, by default it gets 1
  # multiply it with input image to get the segmented image
  # img_cut = img*mask2[:,:,np.newaxis]

  return mask2


def rgb2hex(rgb):
  return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_image_colors(image_path:str, num_colors:int=6) -> List[str]:
  # return ['#ffffff']
  # Read in the image
  img = cv2.imread(image_path)
  # Convert from BGR to RGB
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # scale image to max dimension of 500
  max_dim = 500
  if img.shape[0] > img.shape[1]:
    scale_factor = max_dim / img.shape[0]
  else:
    scale_factor = max_dim / img.shape[1]
  img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)
  print(f'Image shape after resizing: {img.shape} (height, width, channels)')

  foreground_mask = get_foreground_mask(img)
  print('got foreground mask.. saving to file')
  masked_img = img * foreground_mask[:,:,np.newaxis]
  im_name = image_path.partition(".")
  masked_im_path = f'{im_name[0]}_masked.{im_name[2]}'
  print(f'saving masked image to {masked_im_path}...')
  cv2.imwrite(masked_im_path, cv2.cvtColor(masked_img, cv2.COLOR_RGB2BGR))

  # Reshape the image to be a list of pixels
  img = img.reshape((img.shape[0] * img.shape[1], 3))
  reshaped_mask = foreground_mask.reshape((foreground_mask.shape[0] * foreground_mask.shape[1]))
  img = img[reshaped_mask[:] == 1]
  print(f'Image shape after reshaping: {img.shape} (pixels, channels)')

  # Cluster the pixels and assign labels
  clt = KMeans(n_clusters = num_colors)
  labels = clt.fit_predict(img)

  # Count labels to find most popular
  label_counts = Counter(labels)

  # Subset out most popular centroid
  dominant_colors = [clt.cluster_centers_[i] for i in label_counts.keys()]
  # Convert from RGB to hex
  dominant_colors = [rgb2hex(rgb) for rgb in dominant_colors]
  return dominant_colors