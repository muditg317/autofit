import re
from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should only be imported, not run. It contains logic related to a Profile object")

import pickle

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

  @staticmethod
  def load_profile(profile_disk_name: str) -> 'Profile':
    pkl_path = f'{PROFILE_DATA_DIR}/{profile_disk_name}{Profile.SAVE_FILE_SUFFIX}'
    if not os.path.exists(pkl_path):
      raise ValueError(f'Profile {profile_disk_name} does not exist. Run autofit/profiles/create.py to create one.')
    with open(pkl_path, 'rb') as f:
      profile = pickle.load(f)
    return profile
  
  def save_to_disk(self: 'Profile') -> None:
    pkl_path = f'{PROFILE_DATA_DIR}/{self.on_disk_name}{Profile.SAVE_FILE_SUFFIX}'
    with open(pkl_path, 'wb') as f:
      pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

  @staticmethod
  def create_profile() -> 'Profile':
    print('Creating new profile')
    name = input('Enter profile name: ')
    profile = Profile(name=name)
    
    print('Saving empty profile to disk...')
    profile.save_to_disk()
    print('Done!')
    return profile
  
  @staticmethod
  def is_valid_profile_name(profile_name: str) -> None:
    return re.match(r'^[a-zA-Z0-9 _-]+$', profile_name)
