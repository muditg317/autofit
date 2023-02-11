from time import sleep
from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It contains CLI infra for AutoFIT profile editing")
from autofit.cli.question_set import CancellableOrCompletableQuestionSet
from autofit.profiles.profile import Profile

from InquirerPy import inquirer
from InquirerPy.utils import InquirerPyListChoices
from InquirerPy.base.control import Choice

class EditProfileCLI(CancellableOrCompletableQuestionSet[Profile]):
  def __init__(self, profile:Profile) -> None:
    super().__init__()
    self.profile = profile

  def get_message(self) -> str:
    return f"Edit {self.profile.name} profile (changes not saved until exit)..."

  def get_choices(self) -> InquirerPyListChoices:
    choices = []
    choices.append(Choice('add-item', name=f'Add new item (Clothing, Accessory, etc.)'))
    if self.profile.items:
      choices.append(Choice('view-items', name=f'View items'))
    
    return choices

  def can_complete(self) -> bool:
    return True

  def next_default(self) -> str:
    return None

  def handle_choice(self, choice: str) -> None:
    match choice:
      case 'add-item':
        try:
          name = inquirer.text(
            message='Enter item name: ',
            # validate=Profile.is_valid_item_name,
            # invalid_message=Profile.NAME_VALIDITY_MESSAGE
          ).execute().strip()
          image_name = inquirer.text(
            message='Enter image name: ',
            # validate=Profile.is_valid_item_name,
            # invalid_message=Profile.NAME_VALIDITY_MESSAGE
          ).execute().strip()
          description = inquirer.text(
            message='Enter item description: ',
            # validate=Profile.is_valid_item_name,
            # invalid_message=Profile.NAME_VALIDITY_MESSAGE
          ).execute().strip()
          self.profile.add_new_item(name, image_name, description)
        except Exception as e:
          print(f"Error adding item: {e}")
          sleep(0.25)
      case 'view-items':
        item_name = inquirer.select(
          message='Select item to view',
          choices=self.profile.items.keys()
        ).execute()
        print(f"View {item_name}...")
        item = self.profile.items[item_name]
        print(item.name, item.image_path, item.description)
        print('colors:', item.color_info)
      case _:
        raise ValueError(f'Invalid choice {choice}')
    
  def compile(self) -> Profile:
    print("Saving profile updates to disk...")
    self.profile.save_to_disk()
    print("Done!")
