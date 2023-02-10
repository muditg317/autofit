from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It contains CLI infra for AutoFIT profile creation")
from autofit.cli.question_set import CancellableOrCompletableQuestionSet
from autofit.profiles.profile import Profile

from InquirerPy import inquirer
from InquirerPy.utils import InquirerPyListChoices
from InquirerPy.base.control import Choice

class CreateProfileCLI(CancellableOrCompletableQuestionSet[Profile]):
  def __init__(self) -> None:
    super().__init__()
    self.name = ''

  def get_message(self) -> str:
    return f"Add information to new profile..."

  def get_choices(self) -> InquirerPyListChoices:
    return [
      Choice('name', name=f'Set name{f" (currently {self.name})" if self.name else ""}'),
    ]

  def can_complete(self) -> bool:
    return bool(self.name)

  def next_default(self) -> str:
    if not self.name:
      return 'name'

  def handle_choice(self, choice: str) -> None:
    if choice == 'name':
      self.name = inquirer.text(
        message='Enter profile name: ',
        validate=Profile.is_valid_profile_name,
        invalid_message=Profile.NAME_VALIDITY_MESSAGE
      ).execute().strip()
    else:
      raise ValueError(f'Invalid choice {choice}')
    
  def compile(self) -> Profile:
    if not self.name:
      raise ValueError("Profile name is required")
    print("Creating profile...")
    result = Profile(name=self.name)
    print("Saving new profile to disk...")
    result.save_to_disk()
    print("Done!")
    return result
