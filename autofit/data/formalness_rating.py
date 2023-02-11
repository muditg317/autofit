from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It represents formalness information for an AutoFIT item.")

from enum import Enum

class FormalnessRating(Enum):
  CASUAL = 0
  SEMI_FORMAL = 1
  FORMAL = 2
