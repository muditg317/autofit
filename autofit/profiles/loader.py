from autofit.utils.config import *
ASSERT_BEING_RUN(__name__, __file__, "This file should not be imported. It runs `load_profile` in src/profiles/Profile.py")
from autofit.profiles.profile import Profile


def load_from_name(name: str):
  return Profile.load_profile(name)

if __name__ == '__main__':
  profile = load_from_name('test')
  print(profile)