from time import sleep
from typing import Any, Dict, Generic, List, Tuple, TypeVar
from autofit.utils.config import *
ASSERT_NOT_RUN(__name__, __file__, "This file should not be run. It provides infrastructure for the AutoFIT CLI")
from autofit.cli.constants import DEFAULT_STYLE

from abc import ABC, abstractmethod
from InquirerPy import prompt
from InquirerPy.utils import InquirerPySessionResult, InquirerPyQuestions, InquirerPyListChoices
from InquirerPy.base.control import Choice


class QuestionSet(ABC):
  def __init__(self,
      style:Dict[str,str] = DEFAULT_STYLE
    ) -> None:
    self.style = style

  def ask(self) -> InquirerPySessionResult:
    return prompt(self.get_questions(), style=self.style)

  @abstractmethod
  def get_questions(self) -> InquirerPyQuestions:
    pass

  @abstractmethod
  def execute(self) -> Any:
    pass

ResultType = TypeVar('ResultType')
class CancellableOrCompletableQuestionSet(QuestionSet, ABC, Generic[ResultType]):
  def __init__(self,
      choice_name:str = 'user_option',
      style:Dict[str,str] = DEFAULT_STYLE
    ) -> None:
    super().__init__(style)
    self.choice_name = choice_name

  def get_questions(self) -> InquirerPyQuestions:
    choices = self.get_choices()
    if self.can_complete():
      choices.append(Choice('complete', name='Complete'))
    choices.append(Choice('cancel', name='Cancel (changes will be lost)'))
    return [{
      'type': 'list',
      'name': self.choice_name,
      'message': self.get_message(),
      'choices': choices,
      'default': self.next_default() or 'complete'
    }]

  def execute(self) -> ResultType|None:
    while True:
      result = self.ask()
      choice = result[self.choice_name]
      match choice:
        case 'cancel':
          return None
        case 'complete':
          try:
            return self.compile()
          except Exception as e:
            print(f"Cannot complete. Reason: {str(e)}")
            sleep(0.25)
        case _:
          self.handle_choice(choice)

  def get_message(self) -> str:
    return 'What would you like to do?'

  @abstractmethod
  def get_choices(self) -> InquirerPyListChoices:
    pass

  @abstractmethod
  def can_complete(self) -> bool:
    pass

  @abstractmethod
  def next_default(self) -> str:
    pass

  @abstractmethod
  def handle_choice(self, choice: str) -> None:
    pass

  @abstractmethod
  def compile(self) -> ResultType|Exception:
    pass
