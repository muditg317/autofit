from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It represents color information for an AutoFIT item.")
from autofit.cv.image2colors import get_image_colors

from typing import Any, Dict, List

class Color():
  def __init__(self,
      hex:str,
    ) -> None:
    self.hex = hex

  def __str__(self) -> str:
    return self.hex

class ColorInfo:
  def __init__(self,
      colors:List[Color],
    ) -> None:
    self.colors = colors

  def __str__(self) -> str:
    return f"[{', '.join([str(color) for color in self.colors])}]"

  @staticmethod
  def from_image(image_path: str) -> 'ColorInfo':
    colors = get_image_colors(image_path)
    return ColorInfo([Color(color) for color in colors])