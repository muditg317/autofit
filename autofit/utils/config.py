from __future__ import annotations
from autofit.utils.strict_run import *
import os
import sys
# from yaml import safe_load

ASSERT_NOT_RUN(__name__, __file__)

with open('autofit/config.yaml', 'r') as f:
  # config_data = safe_load(f.read())
  config_data = {key.strip(): eval(value.strip()) for key,value in [line.split(':') for line in f.readlines()]}
  # print(config_data)

PROFILE_DATA_DIR = config_data['PROFILE_DATA_DIR']
IMAGE_DATA_DIR = config_data['IMAGE_DATA_DIR']


# Create required directories
DIRS_REQD = [value for key, value in locals().items() if key.endswith('_DIR')]
for entry in DIRS_REQD:
  if not os.path.exists(entry):
    os.makedirs(entry)
