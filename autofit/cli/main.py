from typing import Dict
from autofit.utils.config import *
ASSERT_BEING_RUN(__name__, __file__, "This file should not be imported. It runs the AutoFIT CLI")
from autofit.cli.question_set import QuestionSet
from autofit.cli.create_profile import CreateProfileCLI
from autofit.profiles.profile import Profile

from InquirerPy import prompt, inquirer
from InquirerPy.utils import InquirerPyQuestions
from InquirerPy.base.control import Choice

class BaseQuestionSet(QuestionSet):
  def __init__(self, choice_name:str = 'user_option') -> None:
    super().__init__()
    self.choice_name = choice_name
    self.curr_profile: Profile|None = None
    self.available_profiles: Dict[str, Profile|None] = {name: None for profile_fname in os.listdir(PROFILE_DATA_DIR) if profile_fname.endswith(Profile.SAVE_FILE_SUFFIX) and (name := profile_fname.partition('.')[0])}

  def get_loadable_profiles(self):
    return self.available_profiles if self.curr_profile is None else {name: profile for name, profile in self.available_profiles.items() if name != self.curr_profile.on_disk_name}

  def get_questions(self) -> InquirerPyQuestions:
    choices = []

    if self.curr_profile is not None:
      choices.append(Choice('edit_profile', name=f"Edit profile ({self.curr_profile.on_disk_name})"))

    loadable_profiles = self.get_loadable_profiles()
    match len(loadable_profiles):
      case 0:
        pass
      case 1:
        choices.append(Choice('switch_profile', name=f"Switch profile ({[*loadable_profiles.keys()][0]})"))
      case _:
        choices.append(Choice('load_profile', name=f"Load profile (available: {', '.join(loadable_profiles.keys())})"))
    
    choices.append(Choice('create_profile', name='Create profile'))
    
    choices.append(Choice('exit', name='Exit AutoFIT'))
    
    
    return  [
      {
        'type': 'list',
        'name': self.choice_name,
        'message': 'What would you like to do?',
        'choices': choices
      }
    ]
  
  def execute(self) -> None:
    while True:
      response = self.ask()
      choice = response[self.choice_name]
      if choice == 'exit':
        return
      self.handle_choice(choice)
  
  def handle_choice(self, choice: str):
    match choice:
      case 'create_profile':
        c = CreateProfileCLI()
        while True:
          new_profile = c.execute()
          if new_profile is None:
            break
          if new_profile.on_disk_name in self.available_profiles:
            print(f"Profile {new_profile.on_disk_name} already exists")
            continue
          self.available_profiles[new_profile.on_disk_name] = new_profile
          self.use_profile(new_profile.on_disk_name)
      case 'switch_profile':
        loadable_profiles = self.get_loadable_profiles()
        profile_name = [*loadable_profiles.keys()][0]
        self.use_profile(profile_name)
      case 'load_profile':
        loadable_profiles = self.get_loadable_profiles()
        profile_name = inquirer.select(
          message='Select a profile to load',
          choices=[*loadable_profiles, Choice('cancel', name='Cancel / Go back')]
        ).execute()
        if profile_name == 'cancel':
          return
        self.use_profile(profile_name)
      case 'edit_profile':
        print(self.curr_profile, self.curr_profile.name, self.curr_profile.on_disk_name)
      case _:
        raise Exception(f"Unkown choice made!! {choice}")

  def use_profile(self, profile_disk_name: str):
    if profile_disk_name not in self.available_profiles:
      raise Exception(f"Profile {profile_disk_name} does not exist!")
    profile = self.available_profiles[profile_disk_name] if self.available_profiles[profile_disk_name] is not None else Profile.load_profile(profile_disk_name)
    self.curr_profile = profile
    self.available_profiles[profile.on_disk_name] = profile

if __name__ == '__main__':
  question_set = BaseQuestionSet()
  try:
    question_set.execute()
  except KeyboardInterrupt as e:
    print("Exiting AutoFIT")