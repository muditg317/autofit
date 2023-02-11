from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It provides the ABC for an AutoFIT item (clothing, accessory, etc.)")
from autofit.data.formalness_rating import FormalnessRating
from autofit.data.color_info import ColorInfo

from abc import ABC
from typing import List


class Item():
  def __init__(self,
      name:str,
      image_path:str,
      description:str,
      color_info:ColorInfo = None,
      formalness:FormalnessRating = FormalnessRating.CASUAL,
      tags:List[str] = None,
      **kwargs
    ) -> None:
    self.name = name
    self.image_path = image_path
    assert os.path.exists(image_path), f"Image path {image_path} does not exist"
    self.description = description
    self.color_info = color_info if color_info else ColorInfo.from_image(image_path)
    self.formalness = formalness
    self.tags = tags if tags else []
