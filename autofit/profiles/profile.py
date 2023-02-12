from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should only be imported, not run. It contains logic related to a Profile object")
from autofit.data.item import Item

import pickle
import re
from typing import Dict, List

class Profile:
  SAVE_FILE_SUFFIX = '.autofit.pkl'
  NAME_VALIDATION_REGEX = r'^[a-zA-Z0-9 _-]+$'
  NAME_VALIDITY_MESSAGE = 'Profile names can only contain letters, numbers, underscores, spaces, and dashes.'

  def __init__(self, name:str) -> None:
    self.name = name
    # string has only letters, numbers, underscores, spaces, and dashes
    if not re.match(Profile.NAME_VALIDATION_REGEX, name):
      raise ValueError(f'Profile name {name} is not a valid Profile name. {Profile.NAME_VALIDITY_MESSAGE}')
    self.on_disk_name = re.sub(r'[ -]+', '_', name)
    self.items: Dict[str,Item] = {}

  def add_new_item(self, name:str, image_name:str, description:str) -> None:
    if name in self.items:
      raise ValueError(f'Item {name} already exists in profile {self.name}')
    image_path = f'{IMAGE_DATA_DIR}{image_name}'
    if not os.path.exists(image_path):
      raise ValueError(f'Image path {image_path} does not exist')
    if any(item.image_path == image_path for item in self.items.values()):
      raise ValueError(f'Image path {image_path} already exists in profile {self.name}')
    if not description:
      raise ValueError(f'Description for item {name} is empty')
    print(f'Adding new item {name} to profile {self.name}...')
    print(f'Image path: {image_path}')
    print(f'Description: {description}')
    item = Item(name, image_path, description)
    print(f'Item created - colors: {item.color_info}')
    self.items[name] = item
    print('Done!')

  def delete_item(self, name:str) -> None:
    if name not in self.items:
      raise ValueError(f'Item {name} does not exist in profile {self.name}')
    print(f'Deleting item {name} from profile {self.name}...')
    del self.items[name]
    print('Done!')

  @staticmethod
  def is_valid_profile_name(profile_name: str) -> None:
    return re.match(r'^[a-zA-Z0-9 _-]+$', profile_name)
  
  @staticmethod
  def load_profile(profile_disk_name: str) -> 'Profile':
    pkl_path = f'{PROFILE_DATA_DIR}/{profile_disk_name}{Profile.SAVE_FILE_SUFFIX}'
    if not os.path.exists(pkl_path):
      raise ValueError(f'Profile {profile_disk_name} does not exist. Run autofit/profiles/create.py to create one.')
    with open(pkl_path, 'rb') as f:
      profile = pickle.load(f)
    if 'items' not in profile.__dict__:
      profile.items = {}
    return profile
  
  def save_to_disk(self: 'Profile') -> None:
    pkl_path = f'{PROFILE_DATA_DIR}/{self.on_disk_name}{Profile.SAVE_FILE_SUFFIX}'
    with open(pkl_path, 'wb') as f:
      pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
  
  @staticmethod
  def delete_profile(profile_disk_name: str) -> None:
    pkl_path = f'{PROFILE_DATA_DIR}/{profile_disk_name}{Profile.SAVE_FILE_SUFFIX}'
    if not os.path.exists(pkl_path):
      raise ValueError(f'Profile {profile_disk_name} does not exist. Cannot delete!')
    os.remove(pkl_path)
