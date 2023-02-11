from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It contains helper methods for extracting color information from images.")

# import cv2
# import numpy as np
# from sklearn.cluster import KMeans
# from collections import Counter
# from skimage.color import rgb2lab, deltaE_cie76
# import os
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
from typing import List

def get_foreground_mask(image):
  pass

def get_image_colors(image_path:str, num_colors:int=5) -> List[str]:
  return ['#ffffff']
  # # Read in the image
  # img = cv2.imread(image_path)
  # # Convert from BGR to RGB
  # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  # # Reshape the image to be a list of pixels
  # img = img.reshape((img.shape[0] * img.shape[1], 3))

  # # Cluster the pixels and assign labels
  # clt = KMeans(n_clusters = num_colors)
  # labels = clt.fit_predict(img)

  # # Count labels to find most popular
  # label_counts = Counter(labels)

  # # Subset out most popular centroid
  # dominant_colors = [clt.cluster_centers_[i] for i in label_counts.keys()]
  # # Convert from RGB to hex
  # dominant_colors = [rgb2hex(rgb) for rgb in dominant_colors]
  # return dominant_colors