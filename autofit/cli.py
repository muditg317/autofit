from autofit.utils.config import *
ASSERT_BEING_RUN(__name__, __file__, "This file should not be imported. It loads/manipulates/saves a Profile object")
from autofit.cli import Profile

from InquirerPy import prompt, get_style
from InquirerPy.validator import NumberValidator

cli_styles = {
    "separator": '#6C6C6C',
    "questionmark": '#FF9D00 bold',
    "selected": '#5F819D',
    "pointer": '#FF9D00 bold',
    "instruction": '',  # default
    "answer": '#5F819D bold',
    "question": '',
}

root_questions = [
  {
    'type': 'list',
    'name': 'user_option',
    'message': 'Welcome to simple calculator',
    'choices': ["sum","difference","product", "divide"]
  }
]

ceate_questions = [
  {
    'type': 'list',
    'name': 'create_option',
    'message': 'Enter profile name',
    'choices': ["change name", "cancel"]
  }
]

questions = [
  {
    'type': 'list',
    'name': 'user_option',
    'message': 'Welcome to simple calculator',
    'choices': ["sum","difference","product", "divide"]
  },

  {
    'type': "input",
    "name": "a",
    "message": "Enter the first number",
    "validate": NumberValidator(),
    "filter": lambda val: int(val)
  },

  {
    'type': "input",
    "name": "b",
    "message": "Enter the second number",
    "validate": NumberValidator(),
    "filter": lambda val: int(val)
  }


]

def add(a, b):
  print(a + b)

def difference(a, b):
  print(a - b)

def product(a, b):
  print(a * b)


def divide(a, b):
  print(a / b)


def main():
  answers = prompt(questions, style=cli_styles)
  # a = answers.get("a")
  # b = answers.get("b")
  # if answers.get("user_option") == "sum":
  #   add(a, b)
  # elif answers.get("user_option") == "difference":
  #   difference(a, b)
  # elif answers.get("user_option") == "product":
  #   product(a, b)
  # elif answers.get("user_option") == "divide":
  #   divide(a, b)


if __name__ == "__main__":
  main()